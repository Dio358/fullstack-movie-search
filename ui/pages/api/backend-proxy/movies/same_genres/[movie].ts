import type { NextApiRequest, NextApiResponse } from "next";
import { proxyToBackend } from "../../../../../utils/api-utils"

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { movie } = req.query;
  await proxyToBackend(req, res, `/movies/same_genres/${movie}`);
}