'use client';

import React from 'react';
import { AlertTriangle } from 'lucide-react';

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tooltip, TooltipTrigger, TooltipContent } from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';

const SelectboxWidget = ({
  id,
  label,
  options = [],
  value,
  onChange,
  placeholder = 'Select an option',
  error,
  className,
}) => {

  const _options = Array.isArray(options) ? options : [];

  return (
    <div
      className={cn(
        'relative inline-block w-[200px]',
        error && 'w-[220px] border-destructive border-2 bg-red-50 rounded-md p-2',
        className
      )}
      id={id}
    >
      {label && (
        <label
          htmlFor={id}
          className={cn(
            'block mb-1 text-sm font-semibold',
            error && 'text-destructive'
          )}
        >
          {label}
        </label>
      )}

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

      <Select value={value} onValueChange={onChange} disabled={!!error}>
        <SelectTrigger
          className={cn(
            'w-full justify-between',
            error && 'bg-red-50 border-destructive focus:ring-destructive'
          )}
          aria-label={placeholder}
        >
          <SelectValue placeholder={placeholder} />
          <span></span>
        </SelectTrigger>
        <SelectContent className="w-[200px] min-w-[200px]">
          {_options.map((option) => (
            <SelectItem key={option} value={option}>
              {option}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {error && (
        <div className="text-destructive italic text-xs mt-2 px-1">
          Unable to display options.
        </div>
      )}
    </div>
  );
};

export default SelectboxWidget;
