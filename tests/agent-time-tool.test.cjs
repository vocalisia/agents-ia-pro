const assert = require('node:assert/strict');
const test = require('node:test');
const { calculate, parse, recommend } = require('../js/agent-time-tool.js');
const example = { volume: 400, share: 60, minutes: 10, review: 1, errors: 10, rework: 5, maintenance: 2, setup: 8 };
test('worked example: 40h avoided minus 4h review, 2h rework, 2h maintenance', () => {
  const r = calculate(example); assert.equal(r.net, 32); assert.equal(r.firstMonth, 24); assert.equal(r.setupMonths, .25);
  assert.ok(Math.abs(r.baseline - r.remaining - 32) < 1e-10);
});
test('zero volume or zero delegation still incurs maintenance', () => {
  for (const override of [{volume: 0}, {share: 0}]) assert.equal(calculate({...example, ...override}).net, -2);
});
test('all delegated tasks reworked and review slower than original preserve losses', () => {
  assert.equal(calculate({...example, errors: 100, rework: 10}).net, -6);
  assert.ok(calculate({...example, review: 20}).net < 0);
  assert.equal(calculate({...example, review: 20}).setupMonths, null);
});
test('blank, negative, infinity, exponent, partial number and out-of-range inputs fail', () => {
  for (const value of ['', ' ', '-1', NaN, Infinity, '1e4', '12abc', null]) assert.equal(calculate({...example, minutes: value}).valid, false);
  for (const key of ['share','errors']) assert.equal(calculate({...example, [key]: 101}).valid, false);
  assert.equal(calculate({...example, volume: 1.5}).valid, false);
});
test('French decimal comma is supported; zero differs from missing', () => {
  assert.equal(parse(' 1,5 ', 'review'), 1.5); assert.equal(parse('0', 'review'), 0);
  assert.equal(calculate({...example, review: ''}).valid, false);
});
test('more review, rework, maintenance cannot improve net time', () => {
  for (const [key, value] of Object.entries({review: 2, errors: 20, rework: 8, maintenance: 5})) assert.ok(calculate({...example, [key]: value}).net < 32);
});
test('full delegation without overhead saves the full baseline', () => {
  const r=calculate({...example, share:100, review:0, errors:0, maintenance:0, setup:0});
  assert.equal(r.remaining,0); assert.equal(r.net,r.baseline); assert.equal(r.setupMonths,0);
});
test('orientation never promotes an unprepared task to an agent', () => {
  assert.match(recommend('no','adaptive'), /Préparez/); assert.match(recommend('yes','fixed'), /workflow/);
  assert.match(recommend('yes','draft'), /supervisé/); assert.match(recommend('yes','adaptive'), /limité/);
});
test('minimum volume is the first integer yielding a strictly positive gain', () => {
  const r = calculate(example);
  assert.equal(r.minimumVolume, 24);
  assert.ok(calculate({...example,volume:23}).net < 0);
  assert.ok(calculate({...example,volume:24}).net > 0);
  assert.equal(calculate({...example,share:100,minutes:10,review:0,errors:0,maintenance:1}).minimumVolume,7);
});
test('no fictitious threshold for nonproductive delegation', () => {
  for (const change of [{share:0},{review:20},{minutes:0}]) assert.equal(calculate({...example,...change}).minimumVolume,null);
  assert.equal(calculate({...example,maintenance:0}).minimumVolume,1);
});
test('French grouped numbers parse but malformed grouping fails', () => {
  for (const text of ['1 000','1\u00a0000','1\u202f000']) assert.equal(parse(text,'volume'),1000);
  assert.equal(parse('1 000,5','minutes'),1000.5);
  for (const text of ['1 00','1 0 00','1\t000','12 34 567']) assert.throws(()=>parse(text,'volume'));
});
