import type { RedisClientType } from "./redisClient";
import data from "./data.json";

const initDB = (redisClient: RedisClientType) => {
  Object.entries(data).forEach(([name, attributes]) => {
    Object.entries(attributes).forEach(([field, value]) => {
      redisClient.hSet(name, field, value);
    });
  });
};

export default initDB;
