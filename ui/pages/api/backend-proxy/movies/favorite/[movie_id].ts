import type { NextApiRequest, NextApiResponse } from "next";
import { proxyToBackend } from "../../../../../utils/api-utils"

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { movie_id } = req.query;
  await proxyToBackend(req, res, `/movies/favorite/${movie_id}`);
}