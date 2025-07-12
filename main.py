{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPjdMlp8Wpx+wUcaDQhHelj",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/quantam665/fastapi-kpa-backend/blob/main/main.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "P16_zCtD48J0",
        "outputId": "e6c8acf1-a901-4f4a-e21b-f063dcbfcc4a"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Authtoken saved to configuration file: /root/.config/ngrok/ngrok.yml\n",
            "🚀 Swagger Docs: https://967839367305.ngrok-free.app/docs\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "INFO:     Started server process [10720]\n",
            "INFO:     Waiting for application startup.\n",
            "INFO:     Application startup complete.\n",
            "INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "INFO:     103.164.46.163:0 - \"GET /docs HTTP/1.1\" 200 OK\n",
            "INFO:     103.164.46.163:0 - \"GET /openapi.json HTTP/1.1\" 200 OK\n"
          ]
        }
      ],
      "source": [
        "# ✅ Install required packages\n",
        "!pip install fastapi uvicorn nest-asyncio sqlalchemy pyngrok \"pydantic[email]\" -q\n",
        "!ngrok config add-authtoken 2yAxXlXEyCxUXbQWe3O1nBydZTp_TDQzgdjZLwopBAa6qiFZ\n",
        "\n",
        "# ✅ Imports\n",
        "from fastapi import FastAPI, Depends\n",
        "from pydantic import BaseModel, EmailStr\n",
        "from sqlalchemy import create_engine, Column, Integer, String\n",
        "from sqlalchemy.orm import sessionmaker, declarative_base, Session\n",
        "import nest_asyncio\n",
        "from pyngrok import ngrok\n",
        "import uvicorn\n",
        "import webbrowser\n",
        "import time\n",
        "\n",
        "# 🔁 Enable nested event loop (for Colab)\n",
        "nest_asyncio.apply()\n",
        "\n",
        "# 🔧 SQLite database setup\n",
        "SQLALCHEMY_DATABASE_URL = \"sqlite:///./formdata.db\"\n",
        "engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={\"check_same_thread\": False})\n",
        "SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)\n",
        "Base = declarative_base()\n",
        "\n",
        "# 🧠 SQLAlchemy Model\n",
        "class FormData(Base):\n",
        "    __tablename__ = \"formdata\"\n",
        "    id = Column(Integer, primary_key=True, index=True)\n",
        "    name = Column(String, nullable=False)\n",
        "    email = Column(String, nullable=False)\n",
        "    phone = Column(String, nullable=False)\n",
        "\n",
        "# ✅ Create table\n",
        "Base.metadata.create_all(bind=engine)\n",
        "\n",
        "# 🔗 DB session dependency\n",
        "def get_db():\n",
        "    db = SessionLocal()\n",
        "    try:\n",
        "        yield db\n",
        "    finally:\n",
        "        db.close()\n",
        "\n",
        "# 📦 Pydantic Schemas\n",
        "class FormDataCreate(BaseModel):\n",
        "    name: str\n",
        "    email: EmailStr\n",
        "    phone: str\n",
        "\n",
        "class FormDataResponse(FormDataCreate):\n",
        "    id: int\n",
        "    model_config = {\n",
        "        \"from_attributes\": True\n",
        "    }\n",
        "\n",
        "# 🚀 Create FastAPI app\n",
        "app = FastAPI(title=\"KPA Form Backend API (Colab Version)\")\n",
        "\n",
        "@app.post(\"/formdata\", response_model=FormDataResponse)\n",
        "def create_form(data: FormDataCreate, db: Session = Depends(get_db)):\n",
        "    form = FormData(**data.dict())\n",
        "    db.add(form)\n",
        "    db.commit()\n",
        "    db.refresh(form)\n",
        "    return form\n",
        "\n",
        "@app.get(\"/formdata\", response_model=list[FormDataResponse])\n",
        "def read_all_formdata(db: Session = Depends(get_db)):\n",
        "    return db.query(FormData).all()\n",
        "\n",
        "# 🌐 Start Ngrok Tunnel\n",
        "# 🌐 Start Ngrok Tunnel\n",
        "tunnel = ngrok.connect(8000)\n",
        "public_url = tunnel.public_url\n",
        "docs_url = f\"{public_url}/docs\"\n",
        "print(f\"🚀 Swagger Docs: {docs_url}\")\n",
        "\n",
        "# 🧠 Auto-open Swagger UI\n",
        "import webbrowser, time\n",
        "time.sleep(2)\n",
        "webbrowser.open(docs_url)\n",
        "\n",
        "# 🧠 Auto-open Swagger UI in browser\n",
        "time.sleep(2)  # wait for server to be ready\n",
        "webbrowser.open(docs_url)\n",
        "\n",
        "# 🔥 Run Uvicorn server\n",
        "uvicorn.run(app, host=\"0.0.0.0\", port=8000)\n",
        "\n"
      ]
    }
  ]
}