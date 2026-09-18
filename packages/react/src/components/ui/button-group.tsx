import type {HTMLAttributes} from 'react';
/** Related actions share a perimeter; this is a group, not a keyboard toolbar. */
export function ButtonGroup({className='',...props}:HTMLAttributes<HTMLDivElement>){
 return <div role="group" className={`bf-button-group ${className}`} {...props}/>;
}
