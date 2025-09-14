import streamlit as st
import openai
import base64
from PIL import Image
import io
from datetime import datetime
import json

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
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# Professional QC Analysis function
def analyze_shoe_image(client, image, angle_name, style_number="", color="", po_number=""):
    """
    Analyze shoe image using OpenAI GPT-4 Vision API with professional QC expertise
    """
    base64_image = encode_image(image)
    
    # COMPREHENSIVE PROFESSIONAL QC INSPECTOR PROMPT
    prompt = f"""
PROFESSIONAL FOOTWEAR QUALITY CONTROL INSPECTION - EXPERT ANALYSIS

INSPECTOR PROFILE:
You are a highly experienced footwear quality control inspector with 15+ years in athletic and fashion footwear manufacturing. You have worked with major brands and understand international quality standards. You are known for your meticulous attention to detail and strict adherence to AQL standards.

CURRENT INSPECTION ASSIGNMENT:
- Order: PO#{po_number}
- Product: {style_number} footwear 
- Color: {color}
- View Angle: {angle_name}
- Quality Standard: AQL 2.5 (Manufacturing Grade A)
- Inspection Type: Pre-shipment final inspection
- Client Requirement: Zero tolerance for critical defects

MANUFACTURING CONTEXT:
This is a final quality inspection before shipment to retail customers. Any defect that reaches the end customer could result in returns, complaints, and brand reputation damage. You must inspect with the understanding that this product will be sold at retail and worn by consumers who expect high quality.

DETAILED DEFECT CLASSIFICATION SYSTEM:

🚨 CRITICAL DEFECTS (ZERO TOLERANCE - Immediate Rejection):
**1. Structural Integrity Issues:**
- Complete or partial **outsole debonding** or separation
- Major **heel defects**: broken, warped, or causing instability/tilt
- **Boot barrel deformation** (elastic band deformation) affecting structural integrity
- **The inside exploded** (major lining failure)
- **The upper is damaged** (tears, holes larger than 1mm)
- Broken or cracked structural components
- **Heel kick** (severe front and back kick deformation)

**2. Safety Hazards:**
- Sharp edges or protruding elements
- **Rubber wire** creating safety risks
- Loose hardware that could cause injury
- Chemical odors or visible contamination
- Unstable heel attachment causing tilt or instability



⚠️ MAJOR DEFECTS (Require Rework - Customer Visible Issues):
**1. Adhesive & Bonding Problems:**
- **Overflowing glue** (visible excess adhesive)
- **The outsole lacks glue** (poor bonding preparation)
- **The outsole combination is not tight** (separation gaps >1mm)
- **The middle skin is glued** improperly
- **The skin is glued** with visible defects
- Poor bonding between upper/midsole/outsole components

**2. Alignment & Shape Defects:**
- **The rear trim strip is skewed**
- **Skewed lines** (edges, spacing misalignment)
- **The toe of the shoe is crooked**
- **Toe defects**: misaligned toe box or irregular cap length
- **The length of the toe cap** inconsistency
- **The back package is high and low** (uneven heel counter)
- Components misaligned or twisted relative to shoe centerline
- **Heel counter defects**: shape/height inconsistent or deformed

**3. Material Deformation:**
- **Mesothelial wrinkles** (significant upper creasing)
- **Wrinkled upper** affecting appearance
- **Inner wrinkles** (lining deformation)
- **The waist is not smooth** (poor lasting)
- **Indentation on the upper** (shape defects)
- Midfoot/shank area irregularities affecting profile

**4. Color and Appearance:**
- **Chromatic aberration** (noticeable color differences)
- Color variation between shoe parts (>2 shade difference)
- Color bleeding or staining between materials
- Uneven dyeing or color patches

**5. Construction Defects:**
- **Upper thread** defects (loose, broken, or improper stitching)
- Poor toe lasting (wrinkles, bubbles, asymmetry)
- Visible gaps between sole and upper (>1mm)
- Misaligned or crooked stitching lines
- Puckering or gathering in upper materials

**6. Hardware and Components:**
- Damaged, bent, or non-functional eyelets
- Broken or damaged lace hooks/D-rings
- Velcro not adhering properly
- Buckle damage or malfunction

**7. Lining and Interior:**
- Lining tears, wrinkles, or separation
- Sock liner/insole misprinting or damage
- Tongue positioning issues (too far left/right)

**8. Sole and Bottom:**
- Outsole molding defects or incomplete patterns
- Midsole compression or deformation
- Heel cap damage or misalignment
- Tread pattern inconsistencies



ℹ️ MINOR DEFECTS (Acceptable within AQL limits):
**1. Surface & Cleanliness Issues:**
- **Cleanliness** defects (surface dirt, dust - cleanable)
- Minor scuff marks (<3mm)
- Small adhesive residue spots
- Temporary marking pen marks
- **Transparency marks** (minor see-through effects)

**2. Finishing Details:**
- Thread ends not trimmed (<3mm length)
- Minor stitching irregularities (straight lines)
- Small material texture variations
- Minor logo/branding imperfections
- **Toe corners** with slight irregularities

**3. Cosmetic Issues:**

- Minor sole texture variations
- Slight asymmetry in non-structural elements
- Minor trim imperfections

ANGLE-SPECIFIC INSPECTION FOCUS:

**FRONT VIEW INSPECTION:**
- Toe cap symmetry and shape consistency
- Lace eyelet alignment and spacing
- Tongue centering and positioning
- Color matching between panels
- Overall toe box shape and lasting quality
- Front stitching line straightness
- Logo placement and quality

**BACK VIEW INSPECTION:**
- Heel counter shape and symmetry
- Back seam alignment and straightness
- Heel tab positioning and attachment
- Ankle collar height consistency
- Back logo/branding placement
- Counter stitching quality
- Heel to sole attachment integrity

**LEFT/RIGHT SIDE INSPECTION:**
- Profile shape consistency and symmetry
- Sole to upper bonding quality
- Waist definition and shaping
- Arch support visibility and positioning
- Side panel alignment and stitching
- Heel pitch and alignment
- Overall silhouette conformity

**TOP VIEW INSPECTION:**
- Tongue positioning and symmetry
- Lace eyelet spacing and alignment
- Upper panel symmetry (left vs right)
- Color consistency across all visible areas
- Stitching line parallelism
- Logo and branding alignment

**SOLE VIEW INSPECTION:**
- Outsole pattern completeness and clarity
- Heel attachment and alignment
- Forefoot flex groove positioning
- Tread depth consistency
- Midsole compression and uniformity
- Any embedded foreign objects
- Sole marking and size confirmation

INSPECTION METHODOLOGY:
1. **Systematic Visual Scan:** Examine the shoe systematically from one end to the other
2. **Lighting Assessment:** Consider if image lighting affects defect visibility
3. **Symmetry Check:** Compare left vs right sides for consistency
4. **Scale Assessment:** Evaluate defect size relative to shoe size
5. **Functionality Impact:** Consider if defect affects shoe performance or durability
6. **Customer Perception:** Would an average consumer notice and be concerned?

QUALITY ASSESSMENT CRITERIA:
- **Good:** No visible defects or only very minor cosmetic issues
- **Fair:** Minor defects present but within acceptable limits
- **Poor:** Major defects present or excessive minor defects

CONFIDENCE LEVEL GUIDELINES:
- **High:** Clear, well-lit image with obvious defects or clearly clean areas
- **Medium:** Adequate image quality with some uncertainty due to angle/lighting
- **Low:** Poor image quality, shadows, or unclear areas affecting assessment

OUTPUT REQUIREMENTS:
Provide your professional assessment in this EXACT JSON format:

{{
    "angle": "{angle_name}",
    "critical_defects": ["Be specific: location + defect type + severity"],
    "major_defects": ["Include exact location and detailed description"], 
    "minor_defects": ["Precise location and nature of defect"],
    "overall_condition": "Good/Fair/Poor",
    "confidence": "High/Medium/Low",
    "inspection_notes": "Professional summary with any concerns about image quality or recommendations"
}}

PROFESSIONAL STANDARDS:
- Apply the same scrutiny you would for premium retail footwear
- Remember that consumers will examine these shoes closely in stores
- Consider that defects may become more pronounced with wear
- Prioritize customer satisfaction and brand reputation
- When in doubt about borderline cases, classify as the higher severity level

INSPECTION DIRECTIVE:
Conduct a thorough, professional quality control inspection of this {angle_name} view. Apply your expertise to identify all visible defects with precision and professional judgment. Your assessment will determine if this product meets manufacturing quality standards for retail distribution.

Focus on this specific angle provide detailed, actionable feedback that would help improve manufacturing processes.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4 with vision capabilities
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
            max_tokens=800,  # Increased for detailed responses
            temperature=0.1  # Low temperature for consistent, factual analysis
        )
        
        # Parse the JSON response
        result_text = response.choices[0].message.content
        
        # Find JSON in the response
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = result_text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            # Fallback if JSON parsing fails
            return {
                "angle": angle_name,
                "critical_defects": [],
                "major_defects": [],
                "minor_defects": [],
                "overall_condition": "Fair",
                "confidence": "Low",
                "inspection_notes": "API response parsing failed - raw response logged"
            }
            
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error for {angle_name}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error analyzing {angle_name}: {str(e)}")
        return None

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
    
    # Apply AQL 2.5 standards (based on sample size of 200 pieces)
    # These are the actual limits from your inspection report
    aql_limits = {
        "critical": 0,  # Zero tolerance for critical defects
        "major": 10,    # Maximum 10 major defects allowed
        "minor": 14     # Maximum 14 minor defects allowed
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

# Enhanced HTML Report Generation
def generate_html_report(export_report, po_number, style_number):
    """Generate a professional HTML report with styling"""
    
    inspection_data = export_report['inspection_summary']
    defect_data = export_report['defect_summary']
    defects = export_report['defect_details']
    
    # Determine result color
    result_colors = {
        "ACCEPT": "#28a745",  # Green
        "REWORK": "#ffc107",  # Yellow
        "REJECT": "#dc3545"   # Red
    }
    
    result_color = result_colors.get(inspection_data['final_result'], "#6c757d")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QC Inspection Report - {po_number}</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #333;
            }}
            
            .report-container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                position: relative;
            }}
            
            .header::before {{
                content: '🔍';
                font-size: 3rem;
                position: absolute;
                top: 15px;
                left: 30px;
                opacity: 0.3;
            }}
            
            .header h1 {{
                margin: 0;
                font-size: 2.2rem;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}
            
            .header .subtitle {{
                margin: 10px 0 0 0;
                font-size: 1rem;
                opacity: 0.9;
                font-style: italic;
            }}
            
            .content {{
                padding: 30px;
            }}
            
            .result-banner {{
                background: {result_color};
                color: white;
                padding: 20px;
                margin: -30px -30px 30px -30px;
                text-align: center;
                font-size: 1.4rem;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 5px solid #667eea;
            }}
            
            .info-item {{
                display: flex;
                align-items: center;
            }}
            
            .info-label {{
                font-weight: bold;
                color: #495057;
                margin-right: 10px;
                min-width: 80px;
            }}
            
            .info-value {{
                color: #212529;
                font-family: 'Courier New', monospace;
                background: white;
                padding: 4px 8px;
                border-radius: 4px;
                border: 1px solid #dee2e6;
            }}
            
            .metrics-container {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin: 30px 0;
            }}
            
            .metric-card {{
                text-align: center;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                position: relative;
                overflow: hidden;
            }}
            
            .metric-card.critical {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a52);
                color: white;
            }}
            
            .metric-card.major {{
                background: linear-gradient(135deg, #feca57, #ff9ff3);
                color: white;
            }}
            
            .metric-card.minor {{
                background: linear-gradient(135deg, #48dbfb, #0abde3);
                color: white;
            }}
            
            .metric-number {{
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .metric-label {{
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                opacity: 0.9;
            }}
            
            .metric-limit {{
                font-size: 0.8rem;
                opacity: 0.8;
                margin-top: 5px;
            }}
            
            .defects-section {{
                margin-top: 30px;
            }}
            
            .section-title {{
                font-size: 1.3rem;
                font-weight: bold;
                color: #495057;
                margin: 25px 0 15px 0;
                padding: 10px 0;
                border-bottom: 2px solid #e9ecef;
                display: flex;
                align-items: center;
            }}
            
            .defect-list {{
                background: #fff;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }}
            
            .defect-item {{
                padding: 12px;
                margin: 8px 0;
                border-radius: 6px;
                border-left: 4px solid;
                display: flex;
                align-items: flex-start;
            }}
            
            .defect-item.critical {{
                background: #fff5f5;
                border-left-color: #dc3545;
                color: #721c24;
            }}
            
            .defect-item.major {{
                background: #fff8e1;
                border-left-color: #ffc107;
                color: #7d4e00;
            }}
            
            .defect-item.minor {{
                background: #e3f2fd;
                border-left-color: #17a2b8;
                color: #0c5460;
            }}
            
            .defect-number {{
                font-weight: bold;
                margin-right: 10px;
                min-width: 25px;
            }}
            
            .no-defects {{
                text-align: center;
                padding: 20px;
                color: #28a745;
                font-style: italic;
                background: #f8fff8;
                border: 1px dashed #28a745;
                border-radius: 6px;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px 30px;
                text-align: center;
                color: #6c757d;
                border-top: 1px solid #e9ecef;
            }}
            
            .footer .logo {{
                font-size: 1.1rem;
                font-weight: bold;
                color: #495057;
            }}
            
            .generated-info {{
                font-size: 0.9rem;
                margin-top: 10px;
            }}
            
            .reason-box {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
                font-weight: 500;
            }}
            
            @media print {{
                body {{ background: white; }}
                .report-container {{ box-shadow: none; }}
            }}
            
            .icon {{
                font-size: 1.2rem;
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="report-container">
            <div class="header">
                <h1>Quality Control Inspection Report</h1>
                <p class="subtitle">AI-Powered Footwear Analysis • AQL 2.5 Standard</p>
            </div>
            
            <div class="content">
                <div class="result-banner">
                    🎯 Final Result: {inspection_data['final_result']}
                </div>
                
                <div class="reason-box">
                    <strong>📋 Decision Rationale:</strong> {export_report['decision_rationale']}
                </div>
                
                <div class="info-grid">
                    <div class="info-item">
                        <span class="info-label">📦 PO Number:</span>
                        <span class="info-value">{inspection_data['po_number']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">👟 Style:</span>
                        <span class="info-value">{inspection_data['style_number']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">🎨 Color:</span>
                        <span class="info-value">{inspection_data['color']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">🏢 Customer:</span>
                        <span class="info-value">{inspection_data['customer']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">👨‍🔬 Inspector:</span>
                        <span class="info-value">{inspection_data['inspector']}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">📅 Date:</span>
                        <span class="info-value">{inspection_data['inspection_date']}</span>
                    </div>
                </div>
                
                <div class="section-title">
                    <span class="icon">📊</span>
                    Defect Summary (AQL 2.5 Standard)
                </div>
                
                <div class="metrics-container">
                    <div class="metric-card critical">
                        <div class="metric-number">{defect_data['critical_count']}</div>
                        <div class="metric-label">🚨 Critical Defects</div>
                        <div class="metric-limit">Limit: {defect_data['aql_limits']['critical']}</div>
                    </div>
                    <div class="metric-card major">
                        <div class="metric-number">{defect_data['major_count']}</div>
                        <div class="metric-label">⚠️ Major Defects</div>
                        <div class="metric-limit">Limit: {defect_data['aql_limits']['major']}</div>
                    </div>
                    <div class="metric-card minor">
                        <div class="metric-number">{defect_data['minor_count']}</div>
                        <div class="metric-label">ℹ️ Minor Defects</div>
                        <div class="metric-limit">Limit: {defect_data['aql_limits']['minor']}</div>
                    </div>
                </div>
                
                <div class="defects-section">
    """
    
    # Critical Defects Section
    html_content += """
                    <div class="section-title">
                        <span class="icon">🚨</span>
                        Critical Defects
                    </div>
                    <div class="defect-list">
    """
    
    if defects['critical_defects']:
        for i, defect in enumerate(defects['critical_defects'], 1):
            html_content += f"""
                        <div class="defect-item critical">
                            <span class="defect-number">{i}.</span>
                            <span>{defect}</span>
                        </div>
            """
    else:
        html_content += '<div class="no-defects">✅ No critical defects found</div>'
    
    html_content += "</div>"
    
    # Major Defects Section
    html_content += """
                    <div class="section-title">
                        <span class="icon">⚠️</span>
                        Major Defects
                    </div>
                    <div class="defect-list">
    """
    
    if defects['major_defects']:
        for i, defect in enumerate(defects['major_defects'], 1):
            html_content += f"""
                        <div class="defect-item major">
                            <span class="defect-number">{i}.</span>
                            <span>{defect}</span>
                        </div>
            """
    else:
        html_content += '<div class="no-defects">✅ No major defects found</div>'
    
    html_content += "</div>"
    
    # Minor Defects Section
    html_content += """
                    <div class="section-title">
                        <span class="icon">ℹ️</span>
                        Minor Defects
                    </div>
                    <div class="defect-list">
    """
    
    if defects['minor_defects']:
        for i, defect in enumerate(defects['minor_defects'], 1):
            html_content += f"""
                        <div class="defect-item minor">
                            <span class="defect-number">{i}.</span>
                            <span>{defect}</span>
                        </div>
            """
    else:
        html_content += '<div class="no-defects">✅ No minor defects found</div>'
    
    html_content += f"""
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div class="logo">🤖 AI Footwear Quality Control Inspector</div>
                <div class="generated-info">
                    Report generated on {inspection_data['inspection_date']} using OpenAI GPT-4 Vision API<br>
                    Powered by advanced computer vision and professional QC expertise
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

# Enhanced Text Report Generation
def generate_styled_text_report(export_report, po_number, style_number):
    """Generate a styled text report with better formatting and emojis"""
    
    inspection_data = export_report['inspection_summary']
    defect_data = export_report['defect_summary']
    defects = export_report['defect_details']
    
    # Create styled separator lines
    main_separator = "═" * 70
    sub_separator = "─" * 70
    section_separator = "•" * 70
    
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

{section_separator}

🎯 FINAL INSPECTION RESULT
{sub_separator}
{result_display}

📝 DECISION RATIONALE:
{export_report['decision_rationale']}

{section_separator}

📊 DEFECT SUMMARY (AQL 2.5 COMPLIANCE)
{sub_separator}
🚨 Critical Defects   : {defect_data['critical_count']:>3} / {defect_data['aql_limits']['critical']:>3} (Limit)
⚠️  Major Defects      : {defect_data['major_count']:>3} / {defect_data['aql_limits']['major']:>3} (Limit)
ℹ️  Minor Defects      : {defect_data['minor_count']:>3} / {defect_data['aql_limits']['minor']:>3} (Limit)

{section_separator}

🚨 CRITICAL DEFECTS (Zero Tolerance)
{sub_separator}"""

    if defects['critical_defects']:
        for i, defect in enumerate(defects['critical_defects'], 1):
            text_report += f"\n❗ {i:2d}. {defect}"
    else:
        text_report += "\n✅ No critical defects identified"

    text_report += f"""

{section_separator}

⚠️ MAJOR DEFECTS (Customer Impact)
{sub_separator}"""

    if defects['major_defects']:
        for i, defect in enumerate(defects['major_defects'], 1):
            text_report += f"\n🔶 {i:2d}. {defect}"
    else:
        text_report += "\n✅ No major defects identified"

    text_report += f"""

{section_separator}

ℹ️ MINOR DEFECTS (Cosmetic Issues)
{sub_separator}"""

    if defects['minor_defects']:
        for i, defect in enumerate(defects['minor_defects'], 1):
            text_report += f"\n🔸 {i:2d}. {defect}"
    else:
        text_report += "\n✅ No minor defects identified"

    text_report += f"""

{main_separator}

🏭 QUALITY ASSURANCE CERTIFICATION
{sub_separator}
This inspection has been conducted in accordance with:
• AQL 2.5 International Quality Standard (ISO 2859-1)
• Professional footwear manufacturing guidelines  
• Customer-specific quality requirements
• Industry best practices for retail footwear

🤖 TECHNOLOGY DETAILS
{sub_separator}
• Analysis Engine    : OpenAI GPT-4 Vision API
• Computer Vision    : Advanced image recognition
• QC Expertise       : 15+ years professional knowledge base
• Processing Time    : Real-time analysis
• Accuracy Level     : Professional grade inspection

📊 REPORT METADATA
{sub_separator}
• Report Generated   : {inspection_data['inspection_date']}
• Document Version   : AI-QC-v2.0
• File Format        : Professional Quality Report
• Certification      : AI-Powered Quality Control System

{main_separator}
🎯 End of Report - AI Footwear Quality Control Inspector
    Transforming Manufacturing QC with Computer Vision
{main_separator}
"""

    return text_report

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
        # Store in session state
        if "openai_client" not in st.session_state:
            st.session_state.openai_client = openai.OpenAI(api_key=api_key)
    else:
        st.warning("⚠️ Please enter your OpenAI API key to proceed")
        st.markdown("[Get API Key →](https://platform.openai.com/api-keys)")

# Main interface
if api_key:
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
    **Instructions:** Upload 4-6 high-quality images from different angles:
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
                image = Image.open(uploaded_file)
                angle_name = angle_names[idx] if idx < len(angle_names) else f"Additional View {idx+1}"
                st.image(image, caption=angle_name,use_container_width=True)
        
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
                st.markdown(f"### Final Result:")
                st.markdown(f"## :{result_colors[final_report['result']]}[{final_report['result']}]")
            
            with col2:
                st.markdown(f"### Reason:")
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
                                thumb_image = Image.open(uploaded_files[idx])
                                st.image(thumb_image, caption=f"{angle_name}", width=150)
                        
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
            
            # Enhanced Export Section with three columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📄 Download JSON Report",
                    data=json.dumps(export_report, indent=2, default=str),
                    file_name=f"QC_Report_{po_number}_{style_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                # Generate HTML report
                html_report = generate_html_report(export_report, po_number, style_number)
                st.download_button(
                    label="🎨 Download HTML Report",
                    data=html_report,
                    file_name=f"QC_Report_{po_number}_{style_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            
            with col3:
                # Generate styled text report
                styled_text_report = generate_styled_text_report(export_report, po_number, style_number)
                st.download_button(
                    label="📝 Download Styled Report",
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



