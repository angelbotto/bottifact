import {describe,it,expect} from 'vitest';
import {emptyTableQuery,queryTableRows,tableCSV} from './src/table-model';
describe('shared table query contract',()=>{
 const rows=[{id:'a',amount:10,city:'Bogotá',date:'2026-09-01'},{id:'b',amount:null,city:'Cali',date:'2026-09-16'},{id:'c',amount:10,city:'Bogota',date:'2026-09-12'}];
 it('keeps missing values last in both orders, ties stable and inputs untouched',()=>{for(const direction of ['asc','desc'] as const){const result=queryTableRows(rows,{...emptyTableQuery(),sort:[{column:'amount',direction}]},r=>r);expect(result.map(r=>r.id)).toEqual(['a','c','b']);}expect(rows.map(r=>r.id)).toEqual(['a','b','c']);});
 it('combines facets, accent-insensitive search and ISO date ranges',()=>{const result=queryTableRows(rows,{...emptyTableQuery(),search:'bogota',rules:[{column:'city',operator:'in',value:['Bogota']},{column:'date',operator:'between',value:'2026-09-05',upper:'2026-09-14'}]},r=>r);expect(result.map(r=>r.id)).toEqual(['c']);});
 it('rejects incomplete range values and protects spreadsheet exports',()=>{expect(queryTableRows(rows,{...emptyTableQuery(),rules:[{column:'amount',operator:'gte',value:''}]},r=>r)).toHaveLength(0);expect(tableCSV(['Value'],[[' =cmd()'],[-10],['a"b']])).toBe('"Value"\r\n"\' =cmd()"\r\n"-10"\r\n"a""b"');});
});
