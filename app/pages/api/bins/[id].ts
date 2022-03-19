// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";

import redisClient from "database/redisClient";

import { BinData } from "models/api";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<BinData>
) {
  if (req.method === "GET") {
    const { id } = req.query;
    const data = (await redisClient.hGetAll(id as string)) as BinData;
    res.status(200).json(data);
  }
}
