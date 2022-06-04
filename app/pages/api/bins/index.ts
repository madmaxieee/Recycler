// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";

import redisClient from "database/redisClient";

import { BinData } from "models/api";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<any>
) {
  if (req.method === "GET") {
    const ids = await redisClient.keys("*");
    const results = await Promise.all(ids.map((id) => redisClient.hGetAll(id)));
    res.status(200).json(results);
  }

  if (req.method === "POST") {
    const {
      id,
      data,
    }: {
      id: string;
      data: Record<string, string>;
    } = req.body;


    if (await redisClient.exists(id)) {
    } else {
      Object.entries(data).forEach(([field, value]) =>
        redisClient.hSet(id, field, value)
      );
    }
    res.status(201).send(true);
  }
}
