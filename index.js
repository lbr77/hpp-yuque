async function handleRequest(request) {
    let apiUrl = request.url.replace("yqapi", "")
    request = new Request(apiUrl, request)
    let response = await fetch(request)
    response = new Response(response.body, response)
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.set("Access-Control-Allow-Methods", "*")
    response.headers.set("Access-Control-Allow-Credentials", "true")
    response.headers.set("Access-Control-Allow-Headers", "Content-Type,Access-Token")
    response.headers.set("Access-Control-Expose-Headers", "*")
    return response
}

addEventListener("fetch", event => {
    const request = event.request
    event.respondWith(handleRequest(request))
})