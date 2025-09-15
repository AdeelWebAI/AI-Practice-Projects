import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/hello")
      .then(res => res.json())
      .then(data => setMessage(data.msg))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{textAlign:"center", marginTop:"50px"}}>
      <h1>React + FastAPI</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
