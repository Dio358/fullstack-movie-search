import type { NextApiRequest, NextApiResponse } from "next";

export async function proxyToBackend(
  req: NextApiRequest,
  res: NextApiResponse,
  backendPath: string
) {
  try {
    const backendUrl = `http://app:5000${backendPath}`;

    console.log("handling request to: ", backendUrl)
    
    const options: RequestInit = {
      method: req.method,
      headers: {
        "Content-Type": "application/json",
        ...(req.headers.authorization ? { Authorization: req.headers.authorization as string } : {}),
      }
    };
    
    if (req.method !== "GET" && req.method !== "HEAD") {
      options.body = JSON.stringify(req.body);
    }

    const backendRes = await fetch(backendUrl, options);
    
    const contentType = backendRes.headers.get("Content-Type");
    const data = contentType?.includes("application/json")
      ? await backendRes.json()
      : await backendRes.text();
    
    res.status(backendRes.status).send(data);
  } catch (err: any) {
    console.error("Proxy error:", err);
    res.status(500).json({ error: "Failed to fetch from backend", details: err.message });
  }
}