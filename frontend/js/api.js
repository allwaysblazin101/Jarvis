const API_URL = "http://172.105.110.6:8000"

async function sendToAI(message){

    const res = await fetch(`${API_URL}/reply`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            message: message,
            phone_number: "OWNER_NUMBER"
        })
    })

    const data = await res.json()
    return data.reply
}
