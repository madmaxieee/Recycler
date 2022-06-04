// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";

import redisClient from "database/redisClient";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<any>
) {
  if (req.method === "GET") {
    const { command } = req.query;
    const [id, field, status] = command as string[];
    await redisClient.hSet(id, field, status);
    res.status(200).json(await redisClient.hGet(id, field));
  }
}
