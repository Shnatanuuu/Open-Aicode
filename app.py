import streamlit as st
import openai
import base64
from PIL import Image
import io
from datetime import datetime
import json
import traceback

# Set up the page
st.set_page_config(
    page_title="AI Shoe QC Inspector",
    page_icon="👟",
    layout="wide"
)

st.title("🔍 AI Footwear Quality Control Inspector")
st.markdown("*Powered by OpenAI GPT-4 Vision API*")

# Function to encode image
def encode_image(image):
    """Convert PIL image to base64 string for OpenAI API"""
    try:
        buffer = io.BytesIO()
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA'):
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')
            
        image.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        st.error(f"Error encoding image: {str(e)}")
        return None

# Professional QC Analysis function
def analyze_shoe_image(client, image, angle_name, style_number="", color="", po_number=""):
    """
    Analyze shoe image using OpenAI GPT-4 Vision API with professional QC expertise
    """
    try:
        base64_image = encode_image(image)
        if not base64_image:
            return None
        
        # Simplified but comprehensive prompt
        prompt = f"""
You are a professional footwear quality control inspector analyzing a {angle_name} view of shoe style {style_number}.

Inspect for these defect categories:

CRITICAL DEFECTS (Zero tolerance):
- Sole separation/debonding
- Major structural damage
- Safety hazards
- Wrong product

MAJOR DEFECTS (Customer visible):
- Visible glue overflow
- Misalignment issues
- Shape deformations
- Color variations
- Construction defects
- Poor stitching

MINOR DEFECTS (Cosmetic):
- Small scuffs/marks
- Minor thread ends
- Slight texture variations
- Very small imperfections

Provide assessment in this JSON format:
{{
    "angle": "{angle_name}",
    "critical_defects": ["specific defect descriptions"],
    "major_defects": ["specific defect descriptions"], 
    "minor_defects": ["specific defect descriptions"],
    "overall_condition": "Good/Fair/Poor",
    "confidence": "High/Medium/Low",
    "inspection_notes": "Brief summary of findings"
}}
"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=600,
            temperature=0.1
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Find and parse JSON
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = result_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            # Fallback response
            return {
                "angle": angle_name,
                "critical_defects": [],
                "major_defects": [],
                "minor_defects": ["Analysis parsing error - manual review needed"],
                "overall_condition": "Fair",
                "confidence": "Low",
                "inspection_notes": "API response parsing failed"
            }
            
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error for {angle_name}: {str(e)}")
        return {
            "angle": angle_name,
            "critical_defects": [],
            "major_defects": ["JSON parsing error"],
            "minor_defects": [],
            "overall_condition": "Fair",
            "confidence": "Low",
            "inspection_notes": f"Error: {str(e)}"
        }
    except Exception as e:
        st.error(f"Error analyzing {angle_name}: {str(e)}")
        return {
            "angle": angle_name,
            "critical_defects": [],
            "major_defects": ["Analysis error"],
            "minor_defects": [],
            "overall_condition": "Fair",
            "confidence": "Low",
            "inspection_notes": f"Error: {str(e)}"
        }

# Generate comprehensive QC Report
def generate_qc_report(analyses, order_info):
    """
    Generate final QC report based on all angle analyses and AQL 2.5 standards
    """
    # Combine all defects from all angles
    all_critical = []
    all_major = []
    all_minor = []
    
    for analysis in analyses:
        if analysis:
            all_critical.extend(analysis.get('critical_defects', []))
            all_major.extend(analysis.get('major_defects', []))
            all_minor.extend(analysis.get('minor_defects', []))
    
    # Remove duplicates while preserving order
    all_critical = list(dict.fromkeys(all_critical))
    all_major = list(dict.fromkeys(all_major))
    all_minor = list(dict.fromkeys(all_minor))
    
    # Count defects
    critical_count = len(all_critical)
    major_count = len(all_major)
    minor_count = len(all_minor)
    
    # AQL 2.5 standards
    aql_limits = {
        "critical": 0,  # Zero tolerance
        "major": 10,    # Maximum 10 major defects
        "minor": 14     # Maximum 14 minor defects
    }
    
    # Determine final result
    if critical_count > aql_limits["critical"]:
        result = "REJECT"
        reason = f"Critical defects found ({critical_count}) - Zero tolerance policy"
    elif major_count > aql_limits["major"]:
        result = "REJECT" 
        reason = f"Major defects ({major_count}) exceed AQL limit ({aql_limits['major']})"
    elif minor_count > aql_limits["minor"]:
        result = "REWORK"
        reason = f"Minor defects ({minor_count}) exceed AQL limit ({aql_limits['minor']})"
    else:
        result = "ACCEPT"
        reason = "All defects within acceptable AQL 2.5 limits"
    
    return {
        "result": result,
        "reason": reason,
        "critical_count": critical_count,
        "major_count": major_count,
        "minor_count": minor_count,
        "critical_defects": all_critical,
        "major_defects": all_major,
        "minor_defects": all_minor,
        "aql_limits": aql_limits
    }

# Generate styled text report
def generate_styled_text_report(export_report, po_number, style_number):
    """Generate a styled text report"""
    
    inspection_data = export_report['inspection_summary']
    defect_data = export_report['defect_summary']
    defects = export_report['defect_details']
    
    # Create styled separator lines
    main_separator = "=" * 70
    sub_separator = "-" * 70
    
    # Result styling
    result_symbols = {
        "ACCEPT": "✅ ACCEPTED",
        "REWORK": "🔄 REQUIRES REWORK", 
        "REJECT": "❌ REJECTED"
    }
    
    result_display = result_symbols.get(inspection_data['final_result'], inspection_data['final_result'])
    
    text_report = f"""
{main_separator}
🔍 FOOTWEAR QUALITY CONTROL INSPECTION REPORT
{main_separator}

📋 ORDER INFORMATION
{sub_separator}
📦 PO Number          : {inspection_data['po_number']}
👟 Style Number       : {inspection_data['style_number']}
🎨 Color Code         : {inspection_data['color']}
🏢 Customer           : {inspection_data['customer']}
👨‍🔬 Inspector          : {inspection_data['inspector']}
📅 Inspection Date    : {inspection_data['inspection_date']}
⚡ Standard Applied   : AQL 2.5 International Standard

🎯 FINAL INSPECTION RESULT
{sub_separator}
{result_display}

📝 DECISION RATIONALE:
{export_report['decision_rationale']}

📊 DEFECT SUMMARY (AQL 2.5 COMPLIANCE)
{sub_separator}
🚨 Critical Defects   : {defect_data['critical_count']:>3} / {defect_data['aql_limits']['critical']:>3} (Limit)
⚠️  Major Defects      : {defect_data['major_count']:>3} / {defect_data['aql_limits']['major']:>3} (Limit)
ℹ️  Minor Defects      : {defect_data['minor_count']:>3} / {defect_data['aql_limits']['minor']:>3} (Limit)

🚨 CRITICAL DEFECTS
{sub_separator}"""

    if defects['critical_defects']:
        for i, defect in enumerate(defects['critical_defects'], 1):
            text_report += f"\n❗ {i:2d}. {defect}"
    else:
        text_report += "\n✅ No critical defects identified"

    text_report += f"""

⚠️ MAJOR DEFECTS
{sub_separator}"""

    if defects['major_defects']:
        for i, defect in enumerate(defects['major_defects'], 1):
            text_report += f"\n🔶 {i:2d}. {defect}"
    else:
        text_report += "\n✅ No major defects identified"

    text_report += f"""

ℹ️ MINOR DEFECTS
{sub_separator}"""

    if defects['minor_defects']:
        for i, defect in enumerate(defects['minor_defects'], 1):
            text_report += f"\n🔸 {i:2d}. {defect}"
    else:
        text_report += "\n✅ No minor defects identified"

    text_report += f"""

{main_separator}
🎯 End of Report - AI Footwear Quality Control Inspector
{main_separator}
"""

    return text_report

# Initialize session state
if "openai_client" not in st.session_state:
    st.session_state.openai_client = None

# Sidebar configuration
with st.sidebar:
    st.header("🔧 Configuration")
    st.markdown("**OpenAI Model:** GPT-4 Vision (gpt-4o)")
    
    api_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys"
    )
    
    if api_key:
        st.success("✅ API Key configured!")
        st.info("💡 Cost: ~$0.01-0.03 per image analysis")
        try:
            st.session_state.openai_client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            st.error(f"Error initializing OpenAI client: {str(e)}")
            st.session_state.openai_client = None
    else:
        st.warning("⚠️ Please enter your OpenAI API key to proceed")
        st.markdown("[Get API Key →](https://platform.openai.com/api-keys)")

# Main interface
if st.session_state.openai_client:
    # Order Information Section
    st.header("📋 Order Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        po_number = st.text_input("PO Number", value="0144540", help="Purchase Order Number")
        customer = st.text_input("Customer", value="MIA", help="Customer/Brand Name")
        
    with col2:
        style_number = st.text_input("Style Number", value="GS1412401B", help="Product Style Code")
        color = st.text_input("Color", value="PPB", help="Product Color Code")
        
    with col3:
        inspector = st.text_input("Inspector Name", value="AI Inspector", help="QC Inspector Name")
        inspection_date = st.date_input("Inspection Date", value=datetime.now().date())
    
    st.divider()
    
    # Image Upload Section
    st.header("📸 Upload Shoe Images")
    st.markdown("""
    **Instructions:** Upload 2-6 high-quality images from different angles:
    - 📐 **Front View:** Toe cap, laces, tongue
    - 🔄 **Back View:** Heel, counter, back seam  
    - ↔️ **Side Views:** Left and right profile
    - ⬆️ **Top View:** Overall upper symmetry
    - ⬇️ **Sole View:** Outsole and bottom
    """)
    
    uploaded_files = st.file_uploader(
        "Choose images (JPG, PNG)",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        help="Upload clear, well-lit images from multiple angles"
    )

    if uploaded_files and len(uploaded_files) >= 2:
        st.success(f"✅ {len(uploaded_files)} images uploaded successfully")
        
        # Define standard viewing angles
        angle_names = [
            "Front View", "Back View", "Left Side View", 
            "Right Side View", "Top View", "Sole View"
        ]
        
        # Display uploaded images in grid
        st.subheader("📷 Image Preview")
        cols = st.columns(min(len(uploaded_files), 3))
        
        for idx, uploaded_file in enumerate(uploaded_files):
            col_idx = idx % 3
            with cols[col_idx]:
                try:
                    image = Image.open(uploaded_file)
                    angle_name = angle_names[idx] if idx < len(angle_names) else f"Additional View {idx+1}"
                    st.image(image, caption=angle_name, use_column_width=True)
                except Exception as e:
                    st.error(f"Error displaying image {idx+1}: {str(e)}")
        
        st.divider()
        
        # Analysis Section
        if st.button("🔍 Start AI Quality Inspection", type="primary", use_container_width=True):
            st.header("🤖 AI Analysis in Progress...")
            
            # Progress tracking
            total_images = len(uploaded_files)
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            analyses = []
            
            # Analyze each image
            for idx, uploaded_file in enumerate(uploaded_files):
                angle_name = angle_names[idx] if idx < len(angle_names) else f"Additional View {idx+1}"
                status_text.text(f"🔍 Analyzing {angle_name}... ({idx+1}/{total_images})")
                
                try:
                    image = Image.open(uploaded_file)
                    analysis = analyze_shoe_image(
                        st.session_state.openai_client, 
                        image, 
                        angle_name, 
                        style_number, 
                        color, 
                        po_number
                    )
                    analyses.append(analysis)
                except Exception as e:
                    st.error(f"Error processing image {angle_name}: {str(e)}")
                    analyses.append({
                        "angle": angle_name,
                        "critical_defects": [],
                        "major_defects": [f"Processing error: {str(e)}"],
                        "minor_defects": [],
                        "overall_condition": "Poor",
                        "confidence": "Low",
                        "inspection_notes": f"Image processing failed: {str(e)}"
                    })
                
                progress_bar.progress((idx + 1) / total_images)
            
            status_text.text("✅ Analysis complete! Generating report...")
            
            # Generate final QC report
            order_info = {
                "po_number": po_number,
                "style_number": style_number,
                "color": color,
                "customer": customer,
                "inspector": inspector,
                "inspection_date": inspection_date.strftime("%Y-%m-%d")
            }
            
            final_report = generate_qc_report(analyses, order_info)
            
            st.divider()
            
            # Display Results
            st.header("📊 Quality Control Inspection Report")
            
            # Result Header
            result_colors = {
                "ACCEPT": "success",
                "REWORK": "warning", 
                "REJECT": "error"
            }
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("### Final Result:")
                st.markdown(f"## :{result_colors[final_report['result']]}[{final_report['result']}]")
            
            with col2:
                st.markdown("### Reason:")
                st.markdown(f"**{final_report['reason']}**")
                st.markdown(f"*Inspection completed on {inspection_date.strftime('%B %d, %Y')}*")
            
            # Defect Summary Dashboard
            st.subheader("📈 Defect Summary (AQL 2.5 Standard)")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🚨 Critical Defects", 
                    final_report['critical_count'],
                    delta=f"Limit: {final_report['aql_limits']['critical']}",
                    delta_color="inverse"
                )
                
            with col2:
                major_over_limit = final_report['major_count'] - final_report['aql_limits']['major']
                st.metric(
                    "⚠️ Major Defects", 
                    final_report['major_count'],
                    delta=f"Limit: {final_report['aql_limits']['major']}",
                    delta_color="inverse" if major_over_limit > 0 else "normal"
                )
                
            with col3:
                minor_over_limit = final_report['minor_count'] - final_report['aql_limits']['minor']
                st.metric(
                    "ℹ️ Minor Defects", 
                    final_report['minor_count'],
                    delta=f"Limit: {final_report['aql_limits']['minor']}",
                    delta_color="inverse" if minor_over_limit > 0 else "normal"
                )
            
            # Detailed Defect Lists
            if final_report['critical_defects']:
                st.subheader("🚨 Critical Defects (Must Fix)")
                for i, defect in enumerate(final_report['critical_defects'], 1):
                    st.error(f"**{i}.** {defect}")
            
            if final_report['major_defects']:
                st.subheader("⚠️ Major Defects (Require Attention)")
                for i, defect in enumerate(final_report['major_defects'], 1):
                    st.warning(f"**{i}.** {defect}")
            
            if final_report['minor_defects']:
                st.subheader("ℹ️ Minor Defects (Monitor)")
                for i, defect in enumerate(final_report['minor_defects'], 1):
                    st.info(f"**{i}.** {defect}")
            
            # Individual Angle Analysis
            st.subheader("🔍 Detailed Analysis by View")
            
            for idx, analysis in enumerate(analyses):
                if analysis:
                    angle_name = angle_names[idx] if idx < len(angle_names) else f"Additional View {idx+1}"
                    
                    # Color code based on condition
                    condition_colors = {"Good": "🟢", "Fair": "🟡", "Poor": "🔴"}
                    condition_icon = condition_colors.get(analysis['overall_condition'], "⚫")
                    
                    with st.expander(f"{condition_icon} {angle_name} - {analysis['overall_condition']} (Confidence: {analysis['confidence']})"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            if analysis['critical_defects']:
                                st.markdown("**🚨 Critical:** " + " | ".join(analysis['critical_defects']))
                            if analysis['major_defects']:
                                st.markdown("**⚠️ Major:** " + " | ".join(analysis['major_defects']))
                            if analysis['minor_defects']:
                                st.markdown("**ℹ️ Minor:** " + " | ".join(analysis['minor_defects']))
                            if not any([analysis['critical_defects'], analysis['major_defects'], analysis['minor_defects']]):
                                st.success("✅ No defects detected in this view")
                        
                        with col2:
                            # Show the corresponding image thumbnail
                            if idx < len(uploaded_files):
                                try:
                                    thumb_image = Image.open(uploaded_files[idx])
                                    st.image(thumb_image, caption=f"{angle_name}", width=150)
                                except Exception as e:
                                    st.error(f"Error displaying thumbnail: {str(e)}")
                        
                        if analysis.get('inspection_notes'):
                            st.markdown(f"**Inspector Notes:** {analysis['inspection_notes']}")
            
            # Export Report Section
            st.divider()
            st.subheader("💾 Export Report")
            
            # Prepare comprehensive report data
            export_report = {
                "inspection_summary": {
                    "inspection_date": order_info["inspection_date"],
                    "inspector": order_info["inspector"],
                    "customer": order_info["customer"],
                    "po_number": order_info["po_number"],
                    "style_number": order_info["style_number"],
                    "color": order_info["color"],
                    "final_result": final_report['result'],
                    "inspection_standard": "AQL 2.5"
                },
                "defect_summary": {
                    "critical_count": final_report['critical_count'],
                    "major_count": final_report['major_count'],
                    "minor_count": final_report['minor_count'],
                    "aql_limits": final_report['aql_limits']
                },
                "defect_details": {
                    "critical_defects": final_report['critical_defects'],
                    "major_defects": final_report['major_defects'],
                    "minor_defects": final_report['minor_defects']
                },
                "angle_analyses": analyses,
                "decision_rationale": final_report['reason']
            }
            
            # Export buttons
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📄 Download JSON Report",
                    data=json.dumps(export_report, indent=2, default=str),
                    file_name=f"QC_Report_{po_number}_{style_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                # Generate styled text report
                styled_text_report = generate_styled_text_report(export_report, po_number, style_number)
                st.download_button(
                    label="📝 Download Text Report",
                    data=styled_text_report,
                    file_name=f"QC_Report_{po_number}_{style_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    elif uploaded_files and len(uploaded_files) < 2:
        st.warning("⚠️ Please upload at least 2 images from different angles for proper inspection.")
    else:
        st.info("📤 Please upload shoe images to begin quality inspection.")

else:
    # Landing page when no API key
    st.info("👈 Please enter your OpenAI API key in the sidebar to begin inspection.")
    
    # Show demo information
    st.markdown("---")
    st.subheader("🎯 About This AI QC Inspector")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔧 Features:**
        - Multi-angle shoe analysis
        - Professional defect classification
        - AQL 2.5 standard compliance
        - Detailed inspection reports
        - Export capabilities
        """)
    
    with col2:
        st.markdown("""
        **🎨 Technology:**
        - OpenAI GPT-4 Vision API
        - Real-time image analysis
        - Professional QC expertise
        - Industry-standard reporting
        - Cloud-based processing
        """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🤖 AI Model:** OpenAI GPT-4o Vision")
    
with col2:
    st.markdown("**📊 Standard:** AQL 2.5 Quality Control")
    
with col3:
    st.markdown("**💰 Cost:** ~$0.01-0.03 per image")

st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <em>AI Footwear Quality Control Inspector - Transforming Manufacturing QC with Computer Vision</em>
</div>
""", unsafe_allow_html=True)
