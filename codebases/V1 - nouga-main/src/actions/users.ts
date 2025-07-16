import { db } from '@/db';
import { users } from '@/db/schema';

export async function createUserProfile({
  id,
  name,
  email
}: {
  id: string;
  name: string;
  email: string;
}) {
  await db.insert(users).values({
    id,
    name,
    email,
    created_at: new Date()
  });
}
