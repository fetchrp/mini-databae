GENERATOR_SYSTEM_PROMPT = """
**Prompt:**  
"Given the following database schema and a user query, generate a valid SQL statement that retrieves the requested information. The SQL query should:  

1. **Only perform read operations** (e.g., `SELECT` queries). It should **never** modify the database (i.e., no `INSERT`, `UPDATE`, `DELETE`, `DROP`, or any other write operations).  
2. **Strictly follow the user's request**, ensuring the correct tables, columns, and filters are applied.  
3. **Adhere to the provided schema**, ensuring table names, column names, and relationships are correctly used.  
4. **Use SQL best practices**, including aliasing where appropriate, properly structured `JOIN` operations, and clear formatting for readability.  
5. **If aggregation is required**, use appropriate `GROUP BY` and `HAVING` clauses.  
6. **If filtering is needed**, apply the correct `WHERE` conditions based on the user request.  
7. **If sorting is requested**, use an `ORDER BY` clause in the expected order.  
8. **If limiting results**, use `LIMIT` to restrict the number of returned rows if specified.  

**Schema:**  
(Provide the schema here, including table names, columns, data types, and relationships.)  

**User Query:**  
(Provide the user’s request here.)  

**Expected Output:**  
A properly formatted SQL `SELECT` query that meets the user’s needs without modifying the database."

---
Return only the SQL query with no additional text, explanations, or formatting

"""

REMOVE_DEEPSEEK_THINKING_SQL_PROMPT = """
You must remove all traces of XML and newlines from the output.  
Only return the final SQL query in a clean, single-line format.  
Do not include any explanations, metadata, or additional formatting.  
"""

REMOVE_DEEPSEEK_THINKING_EXPLANATION_PROMPT = """
You must remove all traces of XML from the output.  
Only return the final explanation in a clean, single-line format.  
Do not include any explanations, metadata, or additional formatting.  
"""


ANALYZE_DATA_SET_PROMPT = """
Analyze the provided SQL result set and generate a concise, plain-text summary.  
Provide the actual result set if needed.
Focus on identifying key insights, trends, and patterns in the data.  
Avoid technical jargon, SQL syntax, or complex statistical terms.  
Your response should be clear, human-readable, and actionable.  
"""
