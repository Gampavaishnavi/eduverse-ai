import google.generativeai as genai
from utils.config import Config

# Configure the API key
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)

def get_best_model():
    """Dynamically finds the best available model for the API key."""
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return None
            
        # Prioritize 1.5 flash, then 1.5 pro, then 1.0 pro, then fallback to anything
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-1.0-pro', 'models/gemini-pro']:
            if preferred in available_models:
                return preferred
                
        return available_models[0] # Fallback to first available
    except Exception:
        return 'gemini-1.5-flash' # Ultimate fallback

def get_student_insight(student_data):
    """Generates insights for a specific student."""
    if not Config.GEMINI_API_KEY:
        return "Gemini API Key is not configured. Unable to generate AI insights."
        
    try:
        model_name = get_best_model()
        if not model_name:
            return "No models available for this API key."
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        You are an AI Decision Intelligence Engine for educators.
        Analyze the following student data and provide:
        1. The main reason for their current academic risk.
        2. A personalized, actionable intervention strategy for the faculty.
        
        Student Data:
        Name: {student_data.get('Student_Name', 'Unknown')}
        Attendance: {student_data.get('Attendance', 'N/A')}%
        Assignment Score: {student_data.get('Assignment_Score', 'N/A')}
        Mid Exam: {student_data.get('Mid_Exam', 'N/A')}
        Risk Score: {student_data.get('Risk_Score', 'N/A')}
        Risk Category: {student_data.get('Risk_Category', 'N/A')}
        
        Keep the response concise, professional, and directly actionable.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insight: {e}"

def chat_with_data(query, context_data):
    """General chat interface for faculty to query the dataset."""
    if not Config.GEMINI_API_KEY:
        return "Gemini API Key is not configured."
        
    try:
        model_name = get_best_model()
        if not model_name:
            return "No models available for this API key."
        model = genai.GenerativeModel(model_name)
        prompt = f"""
        You are an AI assistant for the Eduverse AI platform.
        Context (Class Data Summary):
        {context_data}
        
        Faculty Question: {query}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during chat: {e}"
