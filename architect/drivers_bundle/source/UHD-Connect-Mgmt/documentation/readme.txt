Project: rp_uhd_connect.mgmt.driver
Description: UHD Connect management driver — 400G manual RS-FEC on reserve via Configurable setConfig
Category: driver
Class: Community
Tags: Driver, Management, UHD, Connect, Configurable, FEC
CreatedBy: rakesh.kumar@keysight.com
Author: rakesh.kumar@keysight.com
Written and debugged by rakesh.kumar@keysight.com
Co-authored-by: Cursor

Velocity UHD Connect Management Driver

## Requirements
Python on the Agent with requests module installed.

## Supported Functions
setup, verifyReady, teardown, setConfig, getConfig, getProperties, getPorts, getVlans (stub), applyLayer1Profile

## Changelog
1.2.3 Configurable interface; setConfig delegates to setup for RS-FEC (rakesh.kumar@keysight.com)
1.0.0 Initial release
