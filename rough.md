Perfect — here's how to **connect FastAPI + Vue.js** so that your Vue frontend calls an endpoint and receives **streamed responses** as the backend function runs.

---

## ✅ Goal

* Vue fetches a `/query` endpoint
* FastAPI streams output from `query_main(prompt)`
* Vue displays updates in real-time (like a loading terminal)

---

## 🔧 Backend: FastAPI with `StreamingResponse`

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vue app domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example generator function
def query_main(prompt):
    yield f"Intent: {intent_classifier(prompt)}\n"
    yield "Processing...\n"
    yield "Done.\n"

@app.get("/query")
def run_query(prompt: str):
    return StreamingResponse(query_main(prompt), media_type="text/plain")
```

---

## ✅ Frontend: Vue.js Example (Streaming)

You can use the **Fetch API with ReadableStream** to consume the response line-by-line.

### Example Vue Component:

```vue
<template>
  <div>
    <input v-model="prompt" placeholder="Enter your prompt" />
    <button @click="runQuery">Submit</button>
    <pre>{{ result }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      prompt: '',
      result: '',
    };
  },
  methods: {
    async runQuery() {
      this.result = '';
      const response = await fetch(`http://localhost:8000/query?prompt=${encodeURIComponent(this.prompt)}`);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        this.result += decoder.decode(value, { stream: true });
      }
    }
  }
}
</script>
```

---

## 🔄 What Happens

1. User enters a prompt and clicks "Submit"
2. Vue calls `/query` with a `fetch()`
3. FastAPI streams output as `query_main()` yields lines
4. Vue reads the response using `ReadableStream` and updates the UI live

---

## ⚠️ Notes

* Use `CORS` middleware to allow your Vue dev server to access FastAPI
* Don’t use `return` in `query_main()` for intermediate steps — only `yield`
* Make sure `StreamingResponse` uses `media_type="text/plain"` or `text/event-stream`

---

## ✅ Bonus: Want to show a typing animation?

You can append to `this.result` one **character at a time** if you want the "terminal-style" typewriter effect. Let me know if you'd like that!

Would you like me to bundle all of this into a minimal working Vue + FastAPI demo?
