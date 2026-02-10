"""
assistant.py - Natural Language Query Processor for LLMs Powered BI
"""

import pandas as pd
import re


def answer_general_question(query: str) -> str:
    """
    Answer general questions when no data is uploaded.
    
    Args:
        query: User's question
    
    Returns:
        Answer string
    """
    query_lower = query.lower()
    
    # Platform help
    if any(word in query_lower for word in ["help", "how to use", "how do i", "guide", "tutorial"]):
        return """
🎯 **How to Use This Platform:**

1. **Upload Data**: Go to 'Upload Data' page and upload CSV/Excel files
2. **Preview Data**: View your data in 'Data Preview' page
3. **Visualize**: Create charts in 'Visualization' page
4. **Build Dashboard**: Add custom widgets in 'Dashboard Builder'
5. **Get Insights**: View automated insights in 'Insights Dashboard'
6. **Export**: Download reports in 'Export Report' page

💬 **Chat Examples:**
• "Show me top 5 rows"
• "Calculate average of Revenue"
• "What is the total sum?"
• "Display summary statistics"

📂 **First Step**: Upload your data from the 'Upload Data' page to get started!
"""
    
    # What is queries
    elif "what is" in query_lower or "what are" in query_lower or "define" in query_lower:
        # Machine Learning
        if any(term in query_lower for term in ["machine learning", "ml"]):
            return """
🤖 **Machine Learning (ML)** is a branch of artificial intelligence that enables computers to learn from data without being explicitly programmed.

**Key Concepts:**
• **Supervised Learning**: Training with labeled data (e.g., classification, regression)
• **Unsupervised Learning**: Finding patterns in unlabeled data (e.g., clustering)
• **Deep Learning**: Neural networks with multiple layers
• **Training**: Process of teaching the model using data
• **Prediction**: Using trained model on new data

**Common Applications:**
• Image recognition
• Natural language processing
• Recommendation systems
• Fraud detection
"""
        
        # Data Science
        elif "data science" in query_lower:
            return """
📊 **Data Science** is the field of extracting insights and knowledge from structured and unstructured data.

**Key Areas:**
• **Data Collection**: Gathering relevant data
• **Data Cleaning**: Handling missing values, outliers
• **Exploratory Analysis**: Understanding patterns and trends
• **Statistical Modeling**: Building predictive models
• **Visualization**: Presenting insights effectively

**Skills Required:**
• Programming (Python, R)
• Statistics & Mathematics
• Domain Knowledge
• Communication Skills
"""
        
        # Business Intelligence
        elif "business intelligence" in query_lower or "bi" in query_lower:
            return """
💼 **Business Intelligence (BI)** refers to technologies and strategies for analyzing business data.

**Components:**
• **Data Warehousing**: Centralized data storage
• **ETL**: Extract, Transform, Load processes
• **Reporting**: Generating business reports
• **Dashboards**: Visual representation of KPIs
• **Analytics**: Deep-dive analysis

**Benefits:**
• Data-driven decisions
• Improved efficiency
• Competitive advantage
• Better forecasting

**This Platform**: Combines BI with LLMs for natural language data analysis!
"""
        
        # Statistics terms
        elif any(term in query_lower for term in ["mean", "average"]):
            return "📊 **Mean/Average**: Sum of all values divided by count. Shows central tendency. Example: [2,4,6,8] → Mean = 5"
        
        elif "median" in query_lower:
            return "📊 **Median**: Middle value when data is sorted. Less affected by outliers. Example: [1,3,5,7,9] → Median = 5"
        
        elif "standard deviation" in query_lower or "std" in query_lower:
            return "📊 **Standard Deviation**: Measures spread/variability in data. Higher value = more spread out data."
        
        elif any(term in query_lower for term in ["correlation", "relationship"]):
            return "📊 **Correlation**: Measures relationship between two variables. Range: -1 (negative) to +1 (positive). 0 = no correlation."
        
        # Default for "what is"
        else:
            return f"I can explain various concepts! Try asking about:\n• Machine Learning\n• Data Science\n• Business Intelligence\n• Statistical terms (mean, median, correlation)\n\nOr upload data to analyze it!"
    
    # How to queries
    elif "how to" in query_lower or "how do i" in query_lower or "how can i" in query_lower:
        if any(word in query_lower for word in ["analyze", "analysis", "explore"]):
            return """
📊 **How to Analyze Data:**

1. **Upload Data**: Start by uploading your CSV/Excel file
2. **Preview**: Check data quality in 'Data Preview'
3. **Visualize**: Create charts in 'Visualization' page
4. **Get Insights**: View auto-generated insights
5. **Ask Questions**: Use this chat to query your data

💡 **Tips:**
• Start with summary statistics
• Look for trends and patterns
• Check for missing values
• Create multiple visualizations
• Export findings for reports
"""
        
        elif any(word in query_lower for word in ["chart", "graph", "visualize", "plot"]):
            return """
📈 **How to Create Charts:**

1. Go to **'Visualization'** page
2. Upload data if not already done
3. Select X-axis and Y-axis columns
4. Choose chart type (Bar, Line, Pie, etc.)
5. Click 'Generate Chart'

🎨 **Chart Types:**
• **Bar Chart**: Compare categories
• **Line Chart**: Show trends over time
• **Pie Chart**: Show proportions
• **Scatter Plot**: Show relationships
• **Histogram**: Show distributions
• **Box Plot**: Show statistical spread

💡 The platform recommends best chart types based on your data!
"""
        
        else:
            return "I can help with:\n• How to analyze data\n• How to create charts\n• How to use this platform\n\nWhat would you like to know?"
    
    # Capabilities
    elif any(word in query_lower for word in ["can you", "are you able", "do you support"]):
        return """
✨ **My Capabilities:**

📊 **With Data Uploaded:**
• Show top/first N rows
• Calculate statistics (mean, median, sum, count, max, min)
• Detect missing values
• Find correlations
• Generate summaries
• Answer column-specific questions

💬 **Without Data:**
• Explain concepts (ML, Data Science, BI)
• Provide platform guidance
• Define statistical terms
• Give usage tips

🎯 **Best Results**: Upload data first, then ask questions like:
• "Show me top 10 rows"
• "What is the average revenue?"
• "Calculate total sales by region"
"""
    
    # Greeting
    elif any(word in query_lower for word in ["hello", "hi", "hey", "greetings"]):
        return """
👋 **Hello! Welcome to LLMs Powered Business Intelligence!**

I'm your data analysis assistant. I can help you:
• 📂 Analyze uploaded data
• 📊 Explain BI concepts
• 💡 Guide you through the platform
• 🎯 Answer questions about data science, ML, and statistics

**To get started:**
1. Upload your data from the 'Upload Data' page
2. Ask me questions about your data
3. Or ask me to explain any data science concept!

What would you like to know?
"""
    
    # Thank you
    elif any(word in query_lower for word in ["thank", "thanks", "appreciate"]):
        return "You're welcome! 😊 Feel free to ask anything about data analysis, visualization, or upload your data for insights!"
    
    # About platform
    elif any(word in query_lower for word in ["about", "what can you do", "features"]):
        return """
🚀 **LLMs Powered Business Intelligence Platform**

**Features:**
✅ Upload CSV/Excel files
✅ Auto-generate insights
✅ Create interactive visualizations
✅ Build custom dashboards
✅ Natural language queries
✅ Export reports (CSV, JSON, PowerPoint)
✅ Merge multiple datasets
✅ Smart chart recommendations
✅ Time-series analysis

**Technologies:**
• Streamlit (Frontend)
• Pandas (Data Processing)
• Matplotlib (Visualizations)
• Natural Language Processing

**Get Started**: Upload your data to begin analysis!
"""
    
    # Default response
    else:
        return """
🤔 I'm not sure how to answer that yet. Here's what I can help with:

**Without Data:**
• Explain concepts (ask "What is machine learning?")
• Platform guidance (ask "How to use this?")
• Data science terms

**With Data (upload first):**
• "Show me top 10 rows"
• "Calculate average of Revenue"
• "What is the total sum?"
• "Display summary statistics"
• "Find missing values"

📂 **Upload your data** from the 'Upload Data' page to start analyzing!
"""


def process_query(query: str, df: pd.DataFrame) -> str:
    """
    Process natural language queries and return analysis results.
    
    Args:
        query: User's natural language question
        df: Pandas DataFrame to analyze
    
    Returns:
        Formatted string response
    """
    query_lower = query.lower()
    
    try:
        # Handle "top N rows" queries
        if "top" in query_lower and any(x in query_lower for x in ["rows", "records", "5", "10", "3"]):
            num_match = re.findall(r'\d+', query_lower)
            num = int(num_match[0]) if num_match else 5
            return f"📊 Top {num} rows:\n\n" + df.head(num).to_string()
        
        # Handle "first N rows" queries
        elif "first" in query_lower and "rows" in query_lower:
            num_match = re.findall(r'\d+', query_lower)
            num = int(num_match[0]) if num_match else 5
            return f"📊 First {num} rows:\n\n" + df.head(num).to_string()
        
        # Handle mean/average queries
        elif "mean" in query_lower or "average" in query_lower:
            column = _extract_column_name(query, df)
            if column:
                return f"📊 Average of {column}: {df[column].mean():.2f}"
            else:
                return "📊 Average of all numeric columns:\n\n" + df.mean(numeric_only=True).to_string()
        
        # Handle median queries
        elif "median" in query_lower:
            column = _extract_column_name(query, df)
            if column:
                return f"📊 Median of {column}: {df[column].median():.2f}"
            else:
                return "📊 Median of all numeric columns:\n\n" + df.median(numeric_only=True).to_string()
        
        # Handle sum/total queries
        elif "sum" in query_lower or "total" in query_lower:
            column = _extract_column_name(query, df)
            if column:
                return f"📊 Total {column}: {df[column].sum():,.2f}"
            else:
                return "📊 Sum of all numeric columns:\n\n" + df.sum(numeric_only=True).to_string()
        
        # Handle count queries
        elif "count" in query_lower:
            if "rows" in query_lower or "records" in query_lower:
                return f"📊 Total number of rows: {len(df)}"
            else:
                return "📊 Count of non-null values per column:\n\n" + df.count().to_string()
        
        # Handle max/maximum queries
        elif "max" in query_lower or "maximum" in query_lower or "highest" in query_lower:
            column = _extract_column_name(query, df)
            if column:
                max_val = df[column].max()
                max_idx = df[column].idxmax()
                return f"📊 Maximum {column}: {max_val:.2f} (at row index {max_idx})"
            else:
                return "📊 Maximum values for all numeric columns:\n\n" + df.max(numeric_only=True).to_string()
        
        # Handle min/minimum queries
        elif "min" in query_lower or "minimum" in query_lower or "lowest" in query_lower:
            column = _extract_column_name(query, df)
            if column:
                min_val = df[column].min()
                min_idx = df[column].idxmin()
                return f"📊 Minimum {column}: {min_val:.2f} (at row index {min_idx})"
            else:
                return "📊 Minimum values for all numeric columns:\n\n" + df.min(numeric_only=True).to_string()
        
        # Handle describe/summary queries
        elif "describe" in query_lower or "summary" in query_lower or "statistics" in query_lower:
            return "📊 Summary Statistics:\n\n" + df.describe().to_string()
        
        # Handle unique/distinct queries
        elif "unique" in query_lower or "distinct" in query_lower:
            column = _extract_column_name(query, df)
            if column:
                unique_count = df[column].nunique()
                unique_vals = df[column].unique()[:10]  # Show first 10
                return f"📊 Unique values in {column}: {unique_count}\n\nFirst few: {', '.join(map(str, unique_vals))}"
            else:
                result = ["📊 Unique value counts per column:\n"]
                for col in df.columns:
                    result.append(f"{col}: {df[col].nunique()} unique values")
                return "\n".join(result)
        
        # Handle null/missing queries
        elif "null" in query_lower or "missing" in query_lower or "na" in query_lower:
            missing = df.isnull().sum()
            if missing.sum() == 0:
                return "✅ No missing values found in the dataset!"
            else:
                return "⚠️ Missing values per column:\n\n" + missing[missing > 0].to_string()
        
        # Handle correlation queries
        elif "correlat" in query_lower:
            numeric_df = df.select_dtypes(include=['number'])
            if len(numeric_df.columns) < 2:
                return "⚠️ Need at least 2 numeric columns for correlation analysis."
            return "📊 Correlation Matrix:\n\n" + numeric_df.corr().to_string()
        
        # Handle column names query
        elif "columns" in query_lower or "fields" in query_lower:
            return f"📊 Dataset Columns ({len(df.columns)} total):\n\n" + "\n".join([f"• {col}" for col in df.columns])
        
        # Handle data shape query
        elif "shape" in query_lower or "size" in query_lower or "dimensions" in query_lower:
            return f"📊 Dataset Shape:\n• Rows: {len(df)}\n• Columns: {len(df.columns)}\n• Total cells: {len(df) * len(df.columns):,}"
        
        # Handle info query
        elif "info" in query_lower or "information" in query_lower:
            info_str = f"""📊 Dataset Information:

• Rows: {len(df)}
• Columns: {len(df.columns)}
• Numeric columns: {len(df.select_dtypes(include=['number']).columns)}
• Categorical columns: {len(df.select_dtypes(include=['object']).columns)}
• Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB
• Missing values: {df.isnull().sum().sum()}
"""
            return info_str
        
        # Default response
        else:
            return """💡 I couldn't understand that question. Try these examples:

**Basic Queries:**
• "Show me top 10 rows"
• "Display first 5 records"
• "What are the columns?"

**Statistics:**
• "Calculate average of [column]"
• "What is the total sum?"
• "Show me median values"
• "Display summary statistics"

**Data Quality:**
• "Find missing values"
• "Show unique values in [column]"
• "Display correlation matrix"

**Replace [column] with your actual column name!**
"""
    
    except Exception as e:
        return f"⚠️ Error processing query: {str(e)}\n\nPlease rephrase your question or check if the column name is correct."


def _extract_column_name(query: str, df: pd.DataFrame) -> str:
    """
    Extract column name from query by matching against DataFrame columns.
    """
    query_lower = query.lower()
    
    # Try exact match first
    for col in df.columns:
        if col.lower() in query_lower:
            return col
    
    # Try partial match
    for col in df.columns:
        col_words = col.lower().split('_')
        for word in col_words:
            if len(word) > 3 and word in query_lower:
                return col
    
    return ""


def get_auto_insights(df: pd.DataFrame) -> list:
    """
    Generate automatic insights from a DataFrame.
    """
    insights = []
    
    try:
        # Basic info
        insights.append(f"{len(df)} rows and {len(df.columns)} columns")
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            insights.append(f"Numeric columns: {', '.join(numeric_cols[:5])}")
            
            # Find column with highest total
            totals = {col: df[col].sum() for col in numeric_cols}
            max_col = max(totals, key=totals.get)
            insights.append(f"Highest total: {max_col} = {totals[max_col]:,.2f}")
            
            # Find column with highest average
            means = {col: df[col].mean() for col in numeric_cols}
            max_mean_col = max(means, key=means.get)
            insights.append(f"Highest average: {max_mean_col} = {means[max_mean_col]:.2f}")
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            insights.append(f"Categorical columns: {', '.join(categorical_cols[:3])}")
            
            # Most common category
            if len(categorical_cols) > 0:
                first_cat = categorical_cols[0]
                most_common = df[first_cat].value_counts().index[0]
                insights.append(f"Most common {first_cat}: {most_common}")
        
        # Missing values
        missing = df.isnull().sum().sum()
        if missing > 0:
            insights.append(f"⚠️ {missing} missing values detected")
        else:
            insights.append("✅ No missing values")
        
        # Data quality
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            insights.append(f"⚠️ {duplicate_rows} duplicate rows found")
        
    except Exception as e:
        insights.append(f"Error generating insights: {str(e)}")
    
    return insights