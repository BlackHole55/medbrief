import logging
from google import genai
from google.genai import types

from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert clinical AI specialized in translating complex medical notes into clear, empathetic, patient-facing summaries. 

CRITICAL SAFETY DIRECTIVE:
- Rely ONLY on the clear facts directly mentioned in the provided clinical note. 
- Do not assume, extrapolate, or introduce outside clinical conditions, diagnoses, or metrics not explicitly written in the source text.
- If a section below requests information that is completely missing from the clinical note, explicitly output: "Not specified in today's medical record." Do not make up baseline metrics or fill in placeholder data.

Your output MUST be structured into the following four distinct sections, using clear Markdown headings. Do not use dense medical jargon; explain concepts simply.

### 1. What Happened
Summarize the reason for the visit, the history of present illness, and the general timeline of the consultation.

### 2. What We Found
Detail the vital signs, physical exam findings, and any lab or imaging diagnostic results in simple terms.

### 3. Next Steps
Outline the explicit treatment plan, prescribed medications (with dosages if available), follow-up appointments, or pending tests.

### 4. When to Call Us
List specific red flags, worsening symptoms, or warning signs that mean the patient should seek immediate medical attention or contact the clinic.
"""

async def generate_patient_summary(clinical_text: str) -> str:
    """
    Takes raw, jargon-heavy clinical text and uses Gemini to asynchronously
    generate a structured, patient-friendly summary based on the SYSTEM_PROMPT.
    """

    if not settings.GEMINI_API_KEY:
        logger.error("Gemini API key is missing from application settings.")
        raise ValueError("GEMINI_API_KEY config variable is not set.")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        logger.info("Sending clinical text to Gemini for summary generation...")

        response = await client.aio.models.generate_content(
            model='gemini-3.5-flash',
            contents=clinical_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
            ),
        )

        if not response.text:
            logger.warning("Gemini returned an empty response text string.")
            return "Error: Unable to parse clinical text into a summary."
        
        return response.text
    except Exception as e:
        logger.error(f"Failed to generate summary via Gemini API: {str(e)}", exc_info=True)
        raise e