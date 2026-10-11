// 🏢 Part 2: TrunkTools, a small .NET API the agent calls when it needs exact numbers.
//
// Search finds pages; it can't add up a year of bills, and the LLM isn't reliable at maths. So the numbers live in a
// database (trunk.db, filled by ../load_bills.py from the labels the LLM wrote in Part 1: one row per bill), and each
// endpoint is one SQL query. Each endpoint is one TOOL the agent can choose:
//
//   GET /bills?year=1985          SELECT … FROM bills WHERE year = 1985
//   GET /bills/sum?year=1985      SELECT SUM(amount), COUNT(*) FROM bills WHERE year = 1985
//   GET /bills/highest?year=1985  SELECT … WHERE year = 1985 ORDER BY amount DESC LIMIT 1
//
//   python ../load_bills.py   (once)   then   dotnet run   → http://localhost:5085
using Microsoft.Data.Sqlite;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var db = $"Data Source={Path.Combine(builder.Environment.ContentRootPath, "trunk.db")};Mode=ReadOnly";

List<Bill> Query(string sql, int year)
{
    using var con = new SqliteConnection(db);
    con.Open();
    using var cmd = con.CreateCommand();
    cmd.CommandText = sql;
    cmd.Parameters.AddWithValue("$year", year);  // a parameter, never pasted into the SQL text
    using var r = cmd.ExecuteReader();
    var bills = new List<Bill>();
    while (r.Read())
        bills.Add(new Bill(r.GetString(0), r.GetString(1), r.GetDecimal(2)));
    return bills;
}

// The tool inventory: what this API can do for the agent.
app.MapGet("/", () => new[]
{
    new {tool = "GET /bills?year=", does = "every electricity bill for a year"},
    new {tool = "GET /bills/sum?year=", does = "add up a year of electricity bills"},
    new {tool = "GET /bills/highest?year=", does = "the most expensive bill of a year"},
});

app.MapGet("/bills", (int year) =>
    Query("SELECT source, bill_date, amount FROM bills WHERE year = $year ORDER BY source", year));

app.MapGet("/bills/sum", (int year) =>
{
    using var con = new SqliteConnection(db);
    con.Open();
    using var cmd = con.CreateCommand();
    cmd.CommandText = "SELECT SUM(amount), COUNT(*) FROM bills WHERE year = $year";
    cmd.Parameters.AddWithValue("$year", year);
    using var r = cmd.ExecuteReader();
    r.Read();
    var total = r.IsDBNull(0) ? 0m : r.GetDecimal(0);
    var bills = Query("SELECT source, bill_date, amount FROM bills WHERE year = $year ORDER BY source", year);
    return new {year, total, count = r.GetInt32(1), bills, sql = "SELECT SUM(amount), COUNT(*) FROM bills WHERE year = " + year};
});

app.MapGet("/bills/highest", (int year) =>
{
    var top = Query("SELECT source, bill_date, amount FROM bills WHERE year = $year ORDER BY amount DESC LIMIT 1", year).FirstOrDefault();
    return top is null ? Results.NotFound(new {year, message = "no bills for that year"}) : Results.Ok(top);
});

app.Run();

record Bill(string Source, string Date, decimal Amount);
