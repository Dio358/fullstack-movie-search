import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const backendRes = await fetch("http://app:5000/");
    const data = await backendRes.json();
    res.status(200).json(data);
  } catch (err: any) {
    console.error("Proxy error:", err);
    res.status(500).json({ error: "Failed to fetch from backend" });
  }
}