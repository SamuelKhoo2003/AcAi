import base64
import mimetypes
import os
import anthropic 
from fastapi import FastAPI
from fastapi.responses import Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()
origins = [
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = anthropic.Anthropic( 
    api_key = os.environ.get("ANTHROPIC_API_KEY"),
)

def stream_claude_client(prompt: str):
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        temperature=1,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ],
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text

class Outline(BaseModel):
    title: str
    abstract: str

class Outlines(BaseModel):
    data: list[Outline]

@app.post("/generate_outline")
async def generate_outline(outline: Outlines):
    # Extract the data from the request
    data = outline.data
    formatted_data = ""

    for item in data:
        formatted_data += f"""
            {item.title}: {item.abstract}
        """

    prompt = f"""
        Generate an experimental outline for the following research paper. Return a markdown styled answer/outline.
        Don't make the title too large, make it the same size as the headings.

        Involve the following ideas, including their titles and abstracts to form a basis:
        {formatted_data}
    """

    return StreamingResponse(
        stream_claude_client(prompt),
        media_type="text/event-stream"
    )

class CodeRequest(BaseModel):
    plan: str

@app.post("/generate_code")
async def generate_code(req: CodeRequest):
    prompt = f"""
        Generate a code experiment based on the following plan, only generate the code, no other commentary:
        Avoid generating execessive computation and CUDA.
        Please make a simple and TRIVIAL experiment, nothing too complex. Avoid scikit learn and CUDA libraries.
        Format the code using
        ```python
        ```


        This is the experiment plan:
        {req.plan}

        If any plots or images are generated, save them into the image folder such as:
            ```
            IMAGES_FOLDER = "generated_images"
            ...
            plt.savefig(os.path.join(IMAGES_FOLDER, 'graph1.png'))
            ```
    """

    return StreamingResponse(
        stream_claude_client(prompt),
        media_type="text/event-stream"
    )

class SummaryRequest(BaseModel):
    plan: str
    code: str
    image_path: list[str] = []
    output: str

def encode_image_to_base64(image_path):
    """Converts an image to Base64 with its media type."""
    with open(image_path, "rb") as img_file:
        encoded_data = base64.b64encode(img_file.read()).decode("utf-8")
    media_type, _ = mimetypes.guess_type(image_path)
    return encoded_data, media_type or "image/png"

def generate_summary_with_claude(plan, code, output, image_paths):
    """Generates a summary using Claude with text and image inputs."""

    messages_content = []
    prompt = f"""
        Based on the provided information and images, generate a comprehensive summary of the experiment.
        
        Here is the experiment plan:
        {plan}
        
        Code snippet:
        {code}
        
        Output:
        {output}
    """

    # Attach images to the message
    for image_path in image_paths:
        image_data, media_type = encode_image_to_base64(image_path)
        messages_content.append(
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}}
        )
        messages_content.append({"type": "text", "text": "Analyse the image carefully."})

    messages_content.append({"type": "text", "text": prompt})

    # Send request to Claude
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0.7,
        messages=[{"role": "user", "content": messages_content}]
    )

    return message.content[0].text

@app.post("/generate_summary")
async def generate_summary(req: SummaryRequest):

    return Response(
        generate_summary_with_claude(req.plan, req.code, req.output, req.image_path),
        media_type="text/event-stream"
    )
