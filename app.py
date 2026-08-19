import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import re
from groq_client import query_groq  # your Groq client

# Set modern styling
st.set_page_config(page_title="BI Assistant", layout="wide")
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# ---- Initialize session states ----
if "df" not in st.session_state:
    st.session_state.df = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Sidebar ----
st.sidebar.title("LLM'S Powered Business Intelligence Assistant")

# ---- New Chat Button at Top ----
if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.chat_history = []

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to",
    ["📂 Upload Data", "👀 Data Preview", "📊 Visualization", "📈 Insights Dashboard", "🧾 Export Report"]
)

# ---- Chat History in Sidebar ----
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Chat History")
if len(st.session_state.chat_history) == 0:
    st.sidebar.info("No chat history yet.")
else:
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.sidebar.markdown(f"**Q{i}:** {q}")
        st.sidebar.markdown(f"<span style='color:gray;font-size:13px;'>A{i}: {a[:80]}...</span>", unsafe_allow_html=True)
        st.sidebar.markdown("---")

# ---- Clear History Button at Bottom ----
st.sidebar.markdown("---")
col_clear1, col_clear2 = st.sidebar.columns(2)
with col_clear1:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
with col_clear2:
    if st.button("🔄 Clear Data", use_container_width=True):
        st.session_state.df = None
        st.session_state.chat_history = []

# ---- Upload Data ----
if page == "📂 Upload Data":
    st.title("📂 Upload Data")
    uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.df = pd.read_csv(uploaded_file)
        else:
            st.session_state.df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully!")
        if st.session_state.df is not None:
            st.subheader("👀 Quick Data Preview")
            st.dataframe(st.session_state.df.head(), use_container_width=True)

# ---- Data Preview ----
elif page == "👀 Data Preview":
    st.title("👀 Data Preview")
    if st.session_state.df is not None:
        st.dataframe(st.session_state.df, use_container_width=True)
    else:
        st.warning("⚠️ Please upload a dataset first from 'Upload Data'.")

# ---- Enhanced Visualization ----
elif page == "📊 Visualization":
    st.title("📊 Advanced Visualization Studio")
    
    if st.session_state.df is not None:
        df = st.session_state.df
        columns = df.columns.tolist()
        
        # Create two columns for better layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("⚙️ Chart Configuration")
            
            # Chart type selection with icons
            chart_type = st.selectbox(
                "Select Chart Type",
                ["📊 Bar Chart", "📈 Line Chart", "🥧 Pie Chart", "🔵 Scatter Plot", 
                 "📉 Histogram", "📦 Box Plot", "🔥 Heatmap", "🎯 Area Chart"]
            )
            
            # Dynamic axis selection based on chart type
            if "Heatmap" not in chart_type:
                x_col = st.selectbox("Select X-axis", columns)
                
                if chart_type not in ["📉 Histogram", "📦 Box Plot"]:
                    y_col = st.selectbox("Select Y-axis", columns)
                else:
                    y_col = st.selectbox("Select Column", columns)
            
            # Color scheme selection
            color_scheme = st.selectbox(
                "Color Scheme",
                ["Default", "Viridis", "Plasma", "Inferno", "Turbo", "Blues", "Reds", "Greens"]
            )
            
            # Additional options
            show_grid = st.checkbox("Show Grid", value=True)
            interactive = st.checkbox("Interactive (Plotly)", value=True)
            smooth_lines = st.checkbox("Smooth Lines", value=True)
            
            generate_btn = st.button("🎨 Generate Visualization", use_container_width=True)
        
        with col2:
            if generate_btn:
                st.subheader(f"{chart_type}")
                
                # Color palette mapping
                color_map = {
                    "Default": None,
                    "Viridis": "viridis",
                    "Plasma": "plasma",
                    "Inferno": "inferno",
                    "Turbo": "turbo",
                    "Blues": "Blues",
                    "Reds": "Reds",
                    "Greens": "Greens"
                }
                
                try:
                    if interactive:
                        # Plotly Interactive Charts
                        if chart_type == "📊 Bar Chart":
                            grouped_data = df.groupby(x_col)[y_col].sum().reset_index()
                            fig = px.bar(
                                grouped_data, 
                                x=x_col, 
                                y=y_col,
                                color_discrete_sequence=px.colors.qualitative.Set3,
                                template="plotly_white"
                            )
                            fig.update_traces(marker_line_width=1.5, marker_line_color="white")
                            
                        elif chart_type == "📈 Line Chart":
                            fig = px.line(
                                df, 
                                x=x_col, 
                                y=y_col,
                                template="plotly_white",
                                line_shape='spline' if smooth_lines else 'linear'
                            )
                            fig.update_traces(line=dict(width=3))
                            
                        elif chart_type == "🥧 Pie Chart":
                            grouped_data = df.groupby(x_col)[y_col].sum().reset_index()
                            fig = px.pie(
                                grouped_data,
                                names=x_col,
                                values=y_col,
                                hole=0.3,
                                color_discrete_sequence=px.colors.qualitative.Pastel
                            )
                            fig.update_traces(textposition='inside', textinfo='percent+label')
                            
                        elif chart_type == "🔵 Scatter Plot":
                            fig = px.scatter(
                                df,
                                x=x_col,
                                y=y_col,
                                template="plotly_white",
                                opacity=0.7,
                                color_discrete_sequence=['#636EFA']
                            )
                            fig.update_traces(marker=dict(size=10, line=dict(width=1, color='white')))
                            
                        elif chart_type == "📉 Histogram":
                            fig = px.histogram(
                                df,
                                x=y_col,
                                template="plotly_white",
                                color_discrete_sequence=['#AB63FA']
                            )
                            fig.update_traces(marker_line_width=1.5, marker_line_color="white")
                            
                        elif chart_type == "📦 Box Plot":
                            fig = px.box(
                                df,
                                y=y_col,
                                template="plotly_white",
                                color_discrete_sequence=['#00CC96']
                            )
                            
                        elif chart_type == "🔥 Heatmap":
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            corr_matrix = df[numeric_cols].corr()
                            fig = px.imshow(
                                corr_matrix,
                                text_auto='.2f',
                                aspect="auto",
                                color_continuous_scale=color_map.get(color_scheme, 'RdBu_r'),
                                template="plotly_white"
                            )
                            
                        elif chart_type == "🎯 Area Chart":
                            fig = px.area(
                                df,
                                x=x_col,
                                y=y_col,
                                template="plotly_white",
                                line_shape='spline' if smooth_lines else 'linear'
                            )
                            fig.update_traces(line=dict(width=2))
                        
                        # Update layout for all plotly charts
                        fig.update_layout(
                            showlegend=True,
                            hovermode='closest',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(size=12),
                            margin=dict(l=20, r=20, t=40, b=20),
                            xaxis=dict(showgrid=show_grid, gridwidth=1, gridcolor='lightgray'),
                            yaxis=dict(showgrid=show_grid, gridwidth=1, gridcolor='lightgray')
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                    else:
                        # Matplotlib/Seaborn Static Charts with enhanced styling
                        fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
                        
                        if chart_type == "📊 Bar Chart":
                            grouped_data = df.groupby(x_col)[y_col].sum()
                            palette = sns.color_palette(color_map.get(color_scheme, "Set3"), len(grouped_data))
                            grouped_data.plot(kind="bar", ax=ax, color=palette, edgecolor='white', linewidth=1.5)
                            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                            
                        elif chart_type == "📈 Line Chart":
                            if smooth_lines:
                                from scipy.interpolate import make_interp_spline
                                import numpy as np
                                
                                x_numeric = pd.to_numeric(df[x_col], errors='coerce')
                                valid_idx = ~(x_numeric.isna() | df[y_col].isna())
                                x_clean = x_numeric[valid_idx].values
                                y_clean = df[y_col][valid_idx].values
                                
                                if len(x_clean) > 3:
                                    x_sorted_idx = np.argsort(x_clean)
                                    x_sorted = x_clean[x_sorted_idx]
                                    y_sorted = y_clean[x_sorted_idx]
                                    
                                    x_smooth = np.linspace(x_sorted.min(), x_sorted.max(), 300)
                                    spl = make_interp_spline(x_sorted, y_sorted, k=3)
                                    y_smooth = spl(x_smooth)
                                    
                                    ax.plot(x_smooth, y_smooth, linewidth=3, color='#636EFA')
                                else:
                                    df.plot(x=x_col, y=y_col, kind="line", ax=ax, linewidth=3, color='#636EFA')
                            else:
                                df.plot(x=x_col, y=y_col, kind="line", ax=ax, linewidth=3, color='#636EFA')
                            
                        elif chart_type == "🥧 Pie Chart":
                            grouped_data = df.groupby(x_col)[y_col].sum()
                            colors = sns.color_palette(color_map.get(color_scheme, "pastel"), len(grouped_data))
                            grouped_data.plot(
                                kind="pie", 
                                ax=ax, 
                                autopct="%1.1f%%",
                                colors=colors,
                                startangle=90,
                                wedgeprops={'edgecolor': 'white', 'linewidth': 2}
                            )
                            ax.set_ylabel('')
                            
                        elif chart_type == "🔵 Scatter Plot":
                            ax.scatter(df[x_col], df[y_col], alpha=0.7, s=100, 
                                      c='#636EFA', edgecolors='white', linewidth=1)
                            
                        elif chart_type == "📉 Histogram":
                            df[y_col].plot(kind="hist", ax=ax, bins=30, color='#AB63FA', 
                                          edgecolor='white', linewidth=1.5)
                            
                        elif chart_type == "📦 Box Plot":
                            sns.boxplot(y=df[y_col], ax=ax, color='#00CC96', width=0.5)
                            
                        elif chart_type == "🔥 Heatmap":
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            corr_matrix = df[numeric_cols].corr()
                            sns.heatmap(corr_matrix, annot=True, fmt='.2f', ax=ax,
                                       cmap=color_map.get(color_scheme, 'RdBu_r'),
                                       linewidths=1, linecolor='white', square=True)
                            
                        elif chart_type == "🎯 Area Chart":
                            df.plot(x=x_col, y=y_col, kind="area", ax=ax, alpha=0.7, color='#FFA15A')
                        
                        # Enhanced styling
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.grid(show_grid, alpha=0.3, linestyle='--')
                        ax.set_xlabel(ax.get_xlabel(), fontsize=12, fontweight='bold')
                        ax.set_ylabel(ax.get_ylabel(), fontsize=12, fontweight='bold')
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                except Exception as e:
                    st.error(f"❌ Error generating chart: {str(e)}")
                    st.info("💡 Tip: Make sure the selected columns are compatible with the chosen chart type.")
    else:
        st.warning("⚠️ Please upload a dataset first.")

# ---- Insights Dashboard ----
elif page == "📈 Insights Dashboard":
    st.title("📈 Insights Dashboard")
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Rows", f"{len(df):,}")
        with col2:
            st.metric("📋 Total Columns", len(df.columns))
        with col3:
            numeric_cols = df.select_dtypes(include=['number']).columns
            st.metric("🔢 Numeric Columns", len(numeric_cols))
        with col4:
            st.metric("💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        st.markdown("---")
        
        if len(numeric_cols) > 0:
            st.subheader("📊 Summary Statistics")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
            
            # Quick visualization
            st.subheader("📈 Quick Distribution Overview")
            fig = px.box(df[numeric_cols].melt(), y='value', x='variable', 
                        color='variable', template="plotly_white")
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Please upload a dataset first.")

# ---- Export Report ----
elif page == "🧾 Export Report":
    st.title("🧾 Export Report")
    if st.session_state.df is not None:
        csv = st.session_state.df.to_csv(index=False)
        st.download_button("📥 Download CSV", data=csv, file_name="SmartBI_Report.csv", mime="text/csv")
    else:
        st.warning("⚠️ Please upload a dataset first.")

# ---- Chat Interface at Bottom Center ----
st.markdown("""
<style>
.chat-box {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-box">', unsafe_allow_html=True)

# Use a form to prevent auto-rerun
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        query = st.text_input("💬 Ask your question about the data:", key="chat_input", label_visibility="collapsed", placeholder="Type your question here...")
    with col2:
        submit_button = st.form_submit_button("Send", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Process query only when form is submitted
if submit_button and query:
    df = st.session_state.df
    response = ""

    with st.spinner("🤔 Thinking..."):
        try:
            # Send question to Groq API with dataset context if available
            response = query_groq(query, df)

        except Exception as e:
            response = f"❌ Error: {e}"

    # Display the answer
    st.write("**Answer:**")
    st.write(response)

    # Save question & answer in chat history
    st.session_state.chat_history.append((query, response))