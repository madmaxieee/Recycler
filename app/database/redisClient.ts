import * as redis from "redis";
import "dotenv-defaults/config";
import initDB from "./initDB";

const { REDIS_HOST, REDIS_PORT } = process.env;

console.log("redis host:", REDIS_HOST, "\nredis port:", REDIS_PORT);

const redisClient = redis.createClient({
  url: `redis://${REDIS_HOST}:${REDIS_PORT}`,
});

redisClient.connect().then(() => {
  console.log("redis connected");
  initDB(redisClient);
});

redisClient.on("error", (err) => {
  console.log(err);
});

redisClient.on("message", function (channel, key) {
  console.log(channel, key);
});

export type RedisClientType = typeof redisClient;

export default redisClient;
