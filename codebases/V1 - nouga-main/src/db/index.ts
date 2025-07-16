import { config } from 'dotenv';
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

if (process.env.NODE_ENV !== 'production') {
  config({ path: '.env' });
}

const client = postgres(process.env.DATABASE_SESSSION_POOLER!);
export const db = drizzle({ client });
