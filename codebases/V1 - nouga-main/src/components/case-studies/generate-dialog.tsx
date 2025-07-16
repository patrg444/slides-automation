import {
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogClose
} from '@/components/ui/dialog';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { FileText, Presentation } from 'lucide-react';

export default function GenerateDialog() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Select outputs to generate</DialogTitle>
        <DialogDescription>
          A new document will be created, adapting your case study content to
          the template.
        </DialogDescription>
      </DialogHeader>
      <div className='my-6 flex items-stretch gap-4'>
        <button
          className={`flex-1 rounded-lg border p-4 text-left transition-colors ${selected === 'standard' ? 'border-primary bg-primary/5' : 'border-muted bg-background'} hover:border-primary`}
          onClick={() => setSelected('standard')}
        >
          <div className='mb-2 flex items-center gap-2'>
            <span className='mr-2 inline-block h-6 w-6 text-[#7F56D9]'>
              <Presentation size={24} />
            </span>
            <span className='font-semibold'>Standard slide deck (ppt)</span>
          </div>
          <div className='text-muted-foreground text-sm'>
            5 slides comprising of cover page, summary, approach, solution,
            outcomes (success metrics) and project information.
          </div>
        </button>
        <button
          className={`flex-1 flex-col rounded-lg border p-4 text-left transition-colors ${selected === '1pager' ? 'border-primary bg-primary/5' : 'border-muted bg-background'} hover:border-primary`}
          onClick={() => setSelected('1pager')}
        >
          <div className='mb-2 flex items-center gap-2'>
            <span className='mr-2 inline-block h-6 w-6 text-[#7F56D9]'>
              <FileText size={24} />
            </span>
            <span className='font-semibold'>1-pager (ppt)</span>
          </div>
          <div className='text-muted-foreground text-sm'>
            1 slide summary comprising of project name, client name and project
            summary.
          </div>
        </button>
      </div>
      <div className='mt-4 flex justify-end gap-2'>
        <DialogClose asChild>
          <Button variant='outline' type='button'>
            Cancel
          </Button>
        </DialogClose>
        <DialogClose asChild>
          <Button
            className='bg-[#7F56D9] hover:bg-[#7F56D9]/90'
            disabled={!selected}
          >
            Generate
          </Button>
        </DialogClose>
      </div>
    </DialogContent>
  );
}
