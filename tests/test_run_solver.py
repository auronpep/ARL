from tools.run_solver import extract_chat_content, normalize_lm_studio_base_url


def test_normalize_lm_studio_base_url_accepts_openai_style_url():
    assert normalize_lm_studio_base_url("http://127.0.0.1:5962/v1/") == "http://127.0.0.1:5962"


def test_extract_chat_content_ignores_reasoning_content():
    response = {
        "choices": [
            {
                "message": {
                    "content": "\nREADY",
                    "reasoning_content": "internal reasoning",
                }
            }
        ]
    }
    assert extract_chat_content(response) == "\nREADY"
