def load_theme():
    return """
    <style>
    .stApp {
        background-color: #0e0e0e;
        color: white;
    }

    h1 {
        color: #ff2e2e;
        text-align: center;
    }

    div.stButton > button {
        background-color: #ff2e2e;
        color: white;
        border-radius: 10px;
        height: 45px;
        width: 100%;
    }

    .card {
        background-color: #181818;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ff2e2e;
        margin-bottom: 10px;
    }

    @media (max-width: 768px){
        div.stButton > button{
            height: 60px;
            font-size: 18px;
        }
    }
    </style>
    """