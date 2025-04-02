import type { NextApiRequest, NextApiResponse } from "next";

import { proxyToBackend } from "../../../utils/api-utils"

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  await proxyToBackend(req, res, `/login`);
}
