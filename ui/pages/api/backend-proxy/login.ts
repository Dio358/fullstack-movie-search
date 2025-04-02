import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const backendUrl = "http://app:5000/login";
    const backendRes = await fetch(backendUrl, {
      method: req.method,
      headers: {
        "Content-Type": "application/json",
        ...(req.headers.cookie ? { cookie: req.headers.cookie } : {}),
      },
      body: req.method !== "GET" ? JSON.stringify(req.body) : undefined,
    });

    const contentType = backendRes.headers.get("Content-Type");
    let data;
    
    try {
      if (contentType?.includes("application/json")) {
        data = await backendRes.json();
      } else {
        data = await backendRes.text();
      }
    } catch (parseError) {
      console.error("Error parsing response:", parseError);
      return res.status(500).json({ 
        error: "Failed to parse backend response", 
        details: parseError.message 
      });
    }

    res.status(backendRes.status).send(data);
  } catch (err: any) {
    console.error("Proxy error:", err);
    res.status(500).json({ error: "Failed to fetch from backend", details: err.message });
  }
}