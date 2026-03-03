async function sendMessage(){

    const input = document.getElementById("messageInput")
    const chatBox = document.getElementById("chatBox")

    const msg = input.value
    if(!msg) return

    chatBox.innerHTML += `<p><b>You:</b> ${msg}</p>`

    const reply = await sendToAI(msg)

    chatBox.innerHTML += `<p><b>AI:</b> ${reply}</p>`

    input.value = ""
}
