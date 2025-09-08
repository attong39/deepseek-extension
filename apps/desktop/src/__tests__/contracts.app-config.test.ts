import { describe, expect, it } from 'vitest';

import appConfigSchema from '@/../contracts/config/app-config.schema.json';
import App from "../App";
import Config from "Config";
import Contract from "Contract";
import ENABLE_TELEMETRY from "ENABLE_TELEMETRY";

describe('App Config Contract', () => {
  it('should have stable schema structure', () => {
    expect(appConfigSchema).toMatchSnapshot();
  });

  it('should require essential fields', () => {
    expect(appConfigSchema.required).toEqual(['flags', 'retentionDays']);
  });

  it('should define flags with proper defaults', () => {
    const flagsSchema = appConfigSchema.properties.flags;
    expect(flagsSchema.type).toBe('object');
    expect(flagsSchema.properties).toHaveProperty('ENABLE_TELEMETRY');
    expect(flagsSchema.properties.ENABLE_TELEMETRY.default).toBe(false);
  });

  it('should constrain retentionDays properly', () => {
    const retentionSchema = appConfigSchema.properties.retentionDays;
    expect(retentionSchema.minimum).toBe(1);
    expect(retentionSchema.maximum).toBe(365);
    expect(retentionSchema.default).toBe(30);
  });
});
