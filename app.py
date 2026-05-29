demo = gr.ChatInterface(
    fn=ask_ai,
    title="E.E Bot",
    description="Welcome! I am E.E Bot, created by Ebube. Ask me anything!"
)
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
