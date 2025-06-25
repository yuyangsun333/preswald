'use client';

import React from 'react';
import { AlertTriangle } from 'lucide-react';

import { Progress } from '@/components/ui/progress';
import { Tooltip, TooltipTrigger, TooltipContent } from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';

const ProgressWidget = ({ id, value = 0, label, error, className }) => {
  // Ensure value is between 0 and 100
  const normalizedValue = Math.min(Math.max(parseFloat(value) || 0, 0), 100);

  return (
    <div
      id={id}
      className={cn(
        'w-full space-y-2 relative',
        error && 'border-destructive border-2 bg-red-50 rounded-md',
        className
      )}
    >
      {error && (
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="absolute top-2 right-2 text-destructive z-10">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <span>{error.toString()}</span>
          </TooltipContent>
        </Tooltip>
      )}
      {label && (
        <div className="flex justify-between text-sm">
          <span>{label}</span>
          <span>{Math.round(normalizedValue)}%</span>
        </div>
      )}
      {error ? (
        <div className="text-destructive italic text-center py-3">Unable to display progress.</div>
      ) : (
        <Progress value={normalizedValue} />
      )}
    </div>
  );
};

export default ProgressWidget;
