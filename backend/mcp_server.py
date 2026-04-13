from fastmcp import FastMCP
from converter import generate_pdf
import os

# Initialisation du serveur MCP
mcp = FastMCP("Inspirify-PDF-Converter")

@mcp.tool()
def convert_markdown_to_pdf(content: str) -> str:
    """
    Convertit un texte Markdown en fichier PDF professionnel.
    Retourne le chemin local du fichier PDF généré.
    """
    try:
        fname, fpath = generate_pdf(content)
        return f"Succès ! Le PDF a été généré ici : {fpath}"
    except Exception as e:
        return f"Erreur lors de la conversion : {str(e)}"

if __name__ == "__main__":
    import os
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        port = int(os.getenv("MCP_PORT", "8001"))
        print(f"Starting Inspirify-PDF-Converter FastMCP Server via SSE on port {port}...")
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        print("Starting Inspirify-PDF-Converter FastMCP Server via StdIO...")
        mcp.run()
