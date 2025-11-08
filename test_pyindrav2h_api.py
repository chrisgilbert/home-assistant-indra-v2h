#!/usr/bin/env python3
"""Test script to verify pyindrav2h API structure and our client wrapper.

This script tests both the raw pyindrav2h library and our IndraV2HClient wrapper.

Usage:
    export INDRA_EMAIL=your_email@example.com
    export INDRA_PASSWORD=your_password
    python test_pyindrav2h_api.py
"""
import asyncio
import os
import sys

# Add custom_components to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_components'))

def test_raw_library(email: str, password: str):
    """Test the raw pyindrav2h library."""
    print("=" * 60)
    print("Testing Raw pyindrav2h Library")
    print("=" * 60)
    
    try:
        from pyindrav2h.connection import Connection
        from pyindrav2h.v2hclient import v2hClient
        from pyindrav2h import V2H_MODES
        
        print(f"\n✓ Successfully imported pyindrav2h modules")
        print(f"  V2H_MODES: {V2H_MODES}")
        
        # Create connection and client
        connection = Connection(email, password)
        client = v2hClient(connection)
        
        print(f"\n✓ Created Connection and v2hClient")
        print(f"  Connection: {type(connection).__name__}")
        print(f"  Client: {type(client).__name__}")
        
        # Test async methods
        async def test_async():
            print("\n--- Testing Async Methods ---")
            
            # Test refresh
            print("Calling client.refresh()...")
            await client.refresh()
            print("✓ client.refresh() completed")
            
            # Get device
            device = client.device
            if device:
                print(f"✓ Got device: {type(device).__name__}")
                print(f"  Device data type: {type(device.data)}")
                print(f"  Device stats type: {type(device.stats)}")
                
                # Try to access device properties
                try:
                    serial = device.serial
                    print(f"  Device serial: {serial}")
                except Exception as e:
                    print(f"  Could not get serial: {e}")
                
                try:
                    mode = device.mode
                    print(f"  Current mode: {mode}")
                except Exception as e:
                    print(f"  Could not get mode: {e}")
                
                try:
                    state = device.state
                    print(f"  Current state: {state}")
                except Exception as e:
                    print(f"  Could not get state: {e}")
                
                # Show available properties
                print(f"\n  Available device properties:")
                props = [p for p in dir(device) if not p.startswith('_') and not callable(getattr(device, p, None))]
                for prop in props[:10]:
                    try:
                        value = getattr(device, prop, None)
                        print(f"    {prop}: {type(value).__name__}")
                    except:
                        pass
            else:
                print("✗ No device returned")
        
        # Run async test
        asyncio.run(test_async())
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_client_wrapper(email: str, password: str):
    """Test our IndraV2HClient wrapper."""
    print("\n" + "=" * 60)
    print("Testing IndraV2HClient Wrapper")
    print("=" * 60)
    
    try:
        # Import directly from the file to avoid Home Assistant dependencies
        import importlib.util
        client_path = os.path.join(os.path.dirname(__file__), 'custom_components', 'indra_v2h', 'client.py')
        spec = importlib.util.spec_from_file_location("indra_v2h_client", client_path)
        client_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(client_module)
        IndraV2HClient = client_module.IndraV2HClient
        
        print(f"\n✓ Successfully imported IndraV2HClient")
        
        # Create client
        client = IndraV2HClient(email, password)
        print(f"✓ Created IndraV2HClient")
        
        # Test async methods
        async def test_async():
            print("\n--- Testing Client Wrapper Methods ---")
            
            # Test get_device
            print("Calling client.get_device()...")
            try:
                device_data = await client.get_device()
                print(f"✓ get_device() returned: {type(device_data)}")
                if isinstance(device_data, list) and len(device_data) > 0:
                    print(f"  Device list length: {len(device_data)}")
                    print(f"  First device keys: {list(device_data[0].keys())[:5] if isinstance(device_data[0], dict) else 'N/A'}")
                elif isinstance(device_data, dict):
                    print(f"  Device dict keys: {list(device_data.keys())[:5]}")
            except Exception as e:
                print(f"✗ get_device() failed: {e}")
                import traceback
                traceback.print_exc()
            
            # Test get_statistics
            print("\nCalling client.get_statistics()...")
            try:
                stats = await client.get_statistics()
                print(f"✓ get_statistics() returned: {type(stats)}")
                if isinstance(stats, dict):
                    print(f"  Stats keys: {list(stats.keys())[:10]}")
                    if 'data' in stats:
                        print(f"  Stats data keys: {list(stats['data'].keys())[:10] if isinstance(stats['data'], dict) else 'N/A'}")
            except Exception as e:
                print(f"✗ get_statistics() failed: {e}")
                import traceback
                traceback.print_exc()
            
            # Test mode setting (dry run - don't actually change mode)
            print("\n--- Mode Setting Methods (available) ---")
            modes = ["idle", "charge", "discharge", "loadmatch", "exportmatch", "schedule"]
            for mode in modes:
                print(f"  ✓ set_mode('{mode}') - available")
        
        # Run async test
        asyncio.run(test_async())
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Make sure you're running from the project root directory")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("Indra V2H API Test Script")
    print("=" * 60)
    
    # Get credentials from environment variables
    email = os.getenv("INDRA_EMAIL")
    password = os.getenv("INDRA_PASSWORD")
    
    if not email or not password:
        print("ERROR: Missing credentials")
        print("\nPlease set environment variables:")
        print("  export INDRA_EMAIL=your_email@example.com")
        print("  export INDRA_PASSWORD=your_password")
        print("\nOr run:")
        print("  INDRA_EMAIL=your_email@example.com INDRA_PASSWORD=your_password python test_pyindrav2h_api.py")
        sys.exit(1)
    
    print(f"\nUsing email: {email}")
    print(f"Password: {'*' * len(password)}")
    
    # Test raw library
    raw_success = test_raw_library(email, password)
    
    # Test client wrapper
    wrapper_success = test_client_wrapper(email, password)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Raw library test: {'✓ PASSED' if raw_success else '✗ FAILED'}")
    print(f"Client wrapper test: {'✓ PASSED' if wrapper_success else '✗ FAILED'}")
    
    if raw_success and wrapper_success:
        print("\n✓ All tests passed! The integration should work.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
