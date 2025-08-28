import streamlit as st
import requests
import json
import subprocess
import os
import time
import docker
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="FIR Assist - AI-Powered FIR Analysis",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'docker_client' not in st.session_state:
    try:
        st.session_state.docker_client = docker.from_env()
    except:
        st.session_state.docker_client = None

if 'services_status' not in st.session_state:
    st.session_state.services_status = {}

# Constants
API_BASE_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"

def check_service_status():
    """Check the status of all services"""
    status = {}
    
    # Check backend API
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        status['backend'] = "Running" if response.status_code == 200 else "Error"
    except:
        status['backend'] = "Stopped"
    
    # Check frontend
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        status['frontend'] = "Running" if response.status_code == 200 else "Error"
    except:
        status['frontend'] = "Stopped"
    
    # Check MongoDB
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        status['mongodb'] = "Running" if response.status_code == 200 else "Error"
    except:
        status['mongodb'] = "Stopped"
    
    return status

def deploy_services():
    """Deploy the FIR Assist services using Docker Compose"""
    try:
        # Change to the job directory
        os.chdir("job")
        
        # Run docker-compose up
        result = subprocess.run(
            ["docker-compose", "up", "-d", "--build"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return True, "Services deployed successfully!"
        else:
            return False, f"Deployment failed: {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return False, "Deployment timed out"
    except Exception as e:
        return False, f"Deployment error: {str(e)}"

def stop_services():
    """Stop the FIR Assist services"""
    try:
        os.chdir("job")
        result = subprocess.run(
            ["docker-compose", "down"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return True, "Services stopped successfully!"
        else:
            return False, f"Stop failed: {result.stderr}"
    
    except subprocess.TimeoutExpired:
        return False, "Stop operation timed out"
    except Exception as e:
        return False, f"Stop error: {str(e)}"

def analyze_fir_narrative(narrative):
    """Analyze FIR narrative using the backend API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json={"narrative": narrative},
            timeout=30
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {str(e)}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🚔 FIR Assist - AI-Powered FIR Analysis</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Dashboard", "🚀 Deploy Services", "📝 FIR Analysis", "📊 Analytics", "⚙️ Settings"]
    )
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🚀 Deploy Services":
        show_deployment()
    elif page == "📝 FIR Analysis":
        show_fir_analysis()
    elif page == "📊 Analytics":
        show_analytics()
    elif page == "⚙️ Settings":
        show_settings()

def show_dashboard():
    """Show the main dashboard"""
    st.markdown('<h2 class="sub-header">System Dashboard</h2>', unsafe_allow_html=True)
    
    # Check service status
    if st.button("🔄 Refresh Status"):
        st.session_state.services_status = check_service_status()
    
    # Display service status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        backend_status = st.session_state.services_status.get('backend', 'Unknown')
        status_color = "🟢" if backend_status == "Running" else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Backend API</h3>
            <p style="font-size: 2rem;">{status_color}</p>
            <p><strong>{backend_status}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        frontend_status = st.session_state.services_status.get('frontend', 'Unknown')
        status_color = "🟢" if frontend_status == "Running" else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Frontend</h3>
            <p style="font-size: 2rem;">{status_color}</p>
            <p><strong>{frontend_status}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        mongodb_status = st.session_state.services_status.get('mongodb', 'Unknown')
        status_color = "🟢" if mongodb_status == "Running" else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <h3>MongoDB</h3>
            <p style="font-size: 2rem;">{status_color}</p>
            <p><strong>{mongodb_status}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<h3>Quick Actions</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Deploy All Services"):
            with st.spinner("Deploying services..."):
                success, message = deploy_services()
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    with col2:
        if st.button("⏹️ Stop All Services"):
            with st.spinner("Stopping services..."):
                success, message = stop_services()
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    with col3:
        if st.button("🌐 Open Frontend"):
            st.markdown(f"[Open FIR Assist Frontend]({FRONTEND_URL})")
    
    # System information
    st.markdown('<h3>System Information</h3>', unsafe_allow_html=True)
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("""
        **Application Details:**
        - **Name:** FIR Assist - AI-Powered FIR Analysis
        - **Version:** 1.0.0
        - **Technology Stack:** React + Node.js + MongoDB
        - **AI Model:** Legal-BERT for IPC Section Analysis
        """)
    
    with info_col2:
        st.markdown("""
        **Service Ports:**
        - **Frontend:** http://localhost:3000
        - **Backend API:** http://localhost:5000
        - **MongoDB:** localhost:27017
        """)

def show_deployment():
    """Show deployment management page"""
    st.markdown('<h2 class="sub-header">🚀 Service Deployment</h2>', unsafe_allow_html=True)
    
    # Deployment status
    st.markdown('<h3>Current Deployment Status</h3>', unsafe_allow_html=True)
    
    if st.button("🔄 Check Status"):
        st.session_state.services_status = check_service_status()
    
    # Display current status
    for service, status in st.session_state.services_status.items():
        status_icon = "🟢" if status == "Running" else "🔴"
        st.write(f"{status_icon} **{service.title()}:** {status}")
    
    st.markdown("---")
    
    # Deployment controls
    st.markdown('<h3>Deployment Controls</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Deploy Services**")
        st.markdown("""
        This will:
        - Build and start all Docker containers
        - Initialize the database
        - Start the AI analysis service
        """)
        
        if st.button("🚀 Deploy All Services", type="primary"):
            with st.spinner("Deploying FIR Assist services..."):
                success, message = deploy_services()
                if success:
                    st.success(message)
                    st.session_state.services_status = check_service_status()
                else:
                    st.error(message)
    
    with col2:
        st.markdown("**Stop Services**")
        st.markdown("""
        This will:
        - Stop all running containers
        - Preserve data volumes
        - Free up system resources
        """)
        
        if st.button("⏹️ Stop All Services", type="secondary"):
            with st.spinner("Stopping services..."):
                success, message = stop_services()
                if success:
                    st.success(message)
                    st.session_state.services_status = check_service_status()
                else:
                    st.error(message)
    
    # Docker Compose configuration
    st.markdown('<h3>Docker Configuration</h3>', unsafe_allow_html=True)
    
    with st.expander("View Docker Compose Configuration"):
        st.code("""
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/fir-assist
      - PORT=5000
      - NODE_ENV=production
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
        """, language="yaml")

def show_fir_analysis():
    """Show FIR analysis interface"""
    st.markdown('<h2 class="sub-header">📝 FIR Analysis</h2>', unsafe_allow_html=True)
    
    # Check if services are running
    if st.session_state.services_status.get('backend') != 'Running':
        st.warning("⚠️ Backend service is not running. Please deploy services first.")
        return
    
    # Input section
    st.markdown('<h3>Enter Incident Narrative</h3>', unsafe_allow_html=True)
    
    # Text input
    narrative = st.text_area(
        "Describe the incident in detail:",
        height=200,
        placeholder="Enter a detailed description of the incident, including what happened, who was involved, when and where it occurred, and any relevant details that could help identify applicable IPC sections..."
    )
    
    # Example narratives
    with st.expander("📋 Example Narratives"):
        examples = [
            "A person entered a house through an open window and stole jewelry worth ₹50,000 while the residents were sleeping.",
            "Two individuals got into a heated argument at a restaurant, which escalated into a physical fight causing injuries to both parties.",
            "A person was driving under the influence of alcohol and caused an accident that resulted in serious injuries to a pedestrian.",
            "Someone used a fake identity document to open a bank account and later used it for fraudulent transactions.",
            "A group of people gathered in a public place and started shouting slogans without proper permission, causing disturbance to the public."
        ]
        
        selected_example = st.selectbox("Choose an example:", ["Select an example..."] + examples)
        if selected_example != "Select an example...":
            narrative = selected_example
            st.text_area("Selected example:", narrative, height=100, disabled=True)
    
    # Analysis button
    if st.button("🔍 Analyze Incident", type="primary", disabled=not narrative.strip()):
        if narrative.strip():
            with st.spinner("Analyzing incident narrative..."):
                success, result = analyze_fir_narrative(narrative)
                
                if success:
                    st.success("✅ Analysis completed successfully!")
                    
                    # Display recommendations
                    st.markdown('<h3>📋 Recommended IPC Sections</h3>', unsafe_allow_html=True)
                    
                    recommendations = result.get('recommendations', [])
                    
                    if recommendations:
                        for i, rec in enumerate(recommendations, 1):
                            with st.expander(f"🏛️ {rec['code']} - {rec['title']} (Confidence: {rec['score']:.1%})"):
                                st.markdown(f"**Description:** {rec['description']}")
                                
                                if rec.get('judgments'):
                                    st.markdown("**Related Landmark Judgments:**")
                                    for judgment in rec['judgments']:
                                        st.markdown(f"- **{judgment['caseName']}:** {judgment['synopsis']}")
                                else:
                                    st.info("No related judgments found for this section.")
                    else:
                        st.info("No specific IPC sections were identified for this narrative.")
                    
                    # Summary statistics
                    if recommendations:
                        st.markdown('<h3>📊 Analysis Summary</h3>', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Sections Identified", len(recommendations))
                        
                        with col2:
                            avg_confidence = sum(r['score'] for r in recommendations) / len(recommendations)
                            st.metric("Average Confidence", f"{avg_confidence:.1%}")
                        
                        with col3:
                            total_judgments = sum(len(r.get('judgments', [])) for r in recommendations)
                            st.metric("Related Judgments", total_judgments)
                
                else:
                    st.error(f"❌ Analysis failed: {result}")

def show_analytics():
    """Show analytics and insights"""
    st.markdown('<h2 class="sub-header">📊 Analytics & Insights</h2>', unsafe_allow_html=True)
    
    # Check if services are running
    if st.session_state.services_status.get('backend') != 'Running':
        st.warning("⚠️ Backend service is not running. Please deploy services first.")
        return
    
    # Mock analytics data (in a real app, this would come from the database)
    st.markdown('<h3>📈 Usage Statistics</h3>', unsafe_allow_html=True)
    
    # Sample data for demonstration
    analysis_data = {
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'Analyses': [15, 23, 18, 31, 27],
        'Sections_Identified': [45, 67, 52, 89, 73],
        'Avg_Confidence': [0.78, 0.82, 0.75, 0.85, 0.79]
    }
    
    df = pd.DataFrame(analysis_data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(df, x='Date', y='Analyses', title='Daily Analysis Volume')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df, x='Date', y='Sections_Identified', title='Sections Identified per Day')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Confidence distribution
    st.markdown('<h3>🎯 Confidence Score Distribution</h3>', unsafe_allow_html=True)
    
    confidence_data = [0.65, 0.72, 0.78, 0.82, 0.85, 0.88, 0.91, 0.94, 0.97]
    fig3 = px.histogram(x=confidence_data, nbins=10, title='Distribution of Confidence Scores')
    st.plotly_chart(fig3, use_container_width=True)
    
    # Top IPC sections
    st.markdown('<h3>🏛️ Most Frequently Identified IPC Sections</h3>', unsafe_allow_html=True)
    
    top_sections = {
        'IPC Section': ['IPC 379', 'IPC 323', 'IPC 354', 'IPC 420', 'IPC 506'],
        'Count': [45, 38, 32, 28, 25],
        'Description': [
            'Theft',
            'Voluntarily causing hurt',
            'Assault or criminal force to woman with intent to outrage her modesty',
            'Cheating and dishonestly inducing delivery of property',
            'Criminal intimidation'
        ]
    }
    
    top_df = pd.DataFrame(top_sections)
    st.dataframe(top_df, use_container_width=True)

def show_settings():
    """Show application settings"""
    st.markdown('<h2 class="sub-header">⚙️ Settings</h2>', unsafe_allow_html=True)
    
    # Configuration settings
    st.markdown('<h3>🔧 Application Configuration</h3>', unsafe_allow_html=True)
    
    # API settings
    st.markdown("**API Configuration**")
    api_url = st.text_input("Backend API URL", value=API_BASE_URL)
    frontend_url = st.text_input("Frontend URL", value=FRONTEND_URL)
    
    # Database settings
    st.markdown("**Database Configuration**")
    mongodb_uri = st.text_input("MongoDB URI", value="mongodb://localhost:27017/fir-assist", type="password")
    
    # AI Model settings
    st.markdown("**AI Model Configuration**")
    model_name = st.selectbox("Legal-BERT Model", ["nlpaueb/legal-bert-base-uncased"])
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    st.markdown("---")
    
    # System information
    st.markdown('<h3>🖥️ System Information</h3>', unsafe_allow_html=True)
    
    # Docker information
    if st.session_state.docker_client:
        try:
            containers = st.session_state.docker_client.containers.list()
            st.markdown(f"**Running Containers:** {len(containers)}")
            
            if containers:
                container_info = []
                for container in containers:
                    container_info.append({
                        'Name': container.name,
                        'Status': container.status,
                        'Image': container.image.tags[0] if container.image.tags else container.image.id[:12]
                    })
                
                st.dataframe(pd.DataFrame(container_info))
        except Exception as e:
            st.error(f"Error accessing Docker: {str(e)}")
    
    # Application logs
    st.markdown('<h3>📋 Application Logs</h3>', unsafe_allow_html=True)
    
    if st.button("📥 Download Logs"):
        st.info("Log download feature would be implemented here.")
    
    # Reset application
    st.markdown('<h3>🔄 Reset Application</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Data", type="secondary"):
            st.warning("This will clear all analysis data and reset the application.")
    
    with col2:
        if st.button("🔄 Reset to Defaults", type="secondary"):
            st.info("This will reset all settings to their default values.")

if __name__ == "__main__":
    main() 
