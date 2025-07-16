import { NextResponse, NextRequest } from 'next/server';
import { createUserProfile } from '@/actions/users';
import { verifyWebhook } from '@clerk/nextjs/webhooks';

export async function POST(req: NextRequest) {
  try {
    const evt = await verifyWebhook(req);
    console.log('Clerk webhook received', evt);

    if (evt.type === 'user.created') {
      const { id, email_addresses, first_name, last_name } = evt.data;
      const email = email_addresses?.[0]?.email_address || '';
      const name = [first_name, last_name].filter(Boolean).join(' ') || email;
      await createUserProfile({ id, name, email });
      console.log('User profile created');
    }
    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Webhook error:', error);

    return NextResponse.json(
      { error: (error as Error).message },
      { status: 400 }
    );
  }
}

export async function GET() {
  return Response.json({ message: 'Hello World!' });
}
