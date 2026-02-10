from app import get_system_info, get_uptime
from unittest.mock import patch

def test_get_system_info():
    with patch('socket.gethostname', return_value='test-host'), \
        patch('platform.system', return_value='Linux'), \
        patch('platform.version', return_value='#37~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC'), \
        patch('platform.machine', return_value='x86_64'), \
        patch('platform.python_version', return_value='3.13'), \
        patch('os.cpu_count', return_value='4'):
        
        result = get_system_info()
        
        assert result == {
        "hostname": 'test-host',
        "platform_name": 'Linux',
        "platform_version": '#37~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC',
        "architecture": 'x86_64',
        "python_version": '3.13',
        "cpu_count": '4'
    }


def test_get_uptime():
    from datetime import datetime
    
    with patch('app.START_TIME', datetime(2026, 1, 1, 12, 0, 0)), \
         patch('app.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2026, 1, 1, 12, 5, 30)
        
        result = get_uptime()
        
        assert result['seconds'] == 330
        assert result['human'] == '0 hours, 5 minutes'
        assert isinstance(result, dict)
        assert 'seconds' in result
        assert 'human' in result
    
    result = get_uptime()
    assert isinstance(result['seconds'], int)
    assert result['seconds'] >= 0
    assert 'hours' in result['human']
    assert 'minutes' in result['human']
