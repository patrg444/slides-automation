import { createClient } from '@supabase/supabase-js';

export function createSupabaseClient(sessionToken: string | null) {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      global: {
        headers: {
          Authorization: sessionToken ? `Bearer ${sessionToken}` : ''
        }
      }
    }
  );
}
