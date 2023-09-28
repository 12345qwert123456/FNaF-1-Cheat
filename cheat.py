import frida
import time

PROC_NAME = 'FiveNightsatFreddys.exe'
MODULE_NAME = "'FiveNightsatFreddys.exe'"

def on_message(message, data):
    print("[%s] => %s" % (message, data))


def main(target_process):
    session = frida.attach(target_process)
    while True:
        freeze = False
        user_input = input("1. Set energy\n2. Set time\n3. Freeze time\n4. Skip night\n5. Show minutes\n6. Hack door animation\n0. Exit\n: ")
        if int(user_input) == 1:
            energy_percent = int(input("Enter count of energy: "))
            script = session.create_script(set_energy(energy_percent))
        elif int(user_input) == 2:
            hour = int(input("Enter hour: "))
            script = session.create_script(set_time(hour))
        elif int(user_input) == 3:
            script = session.create_script(stop_time())
            freeze = True
        elif int(user_input) == 4:
            script = session.create_script(set_time(6))
        elif int(user_input) == 5:
            script = session.create_script(minutes())
            freeze = True
        elif int(user_input) == 6:
            script = session.create_script(door_hack())
            freeze = True
        elif int(user_input) == 0:
            break
        script.on('message', on_message)
        script.load()
        time.sleep(1)
        if freeze:
            input("\n--Press 'Enter' to back--\n")
        script.unload()
    print("Exit")
    session.detach()


def set_energy(int_percent):
    return f"""
    var module_name_FiveNightsatFreddys_exe={MODULE_NAME};
    var call_count = 0;
    var offset_of_00415363=0x1555f;
    var dynamic_address_of_00415363=Module.findBaseAddress(module_name_FiveNightsatFreddys_exe).add(offset_of_00415363);
    function function_to_call_when_code_reaches_00415363(){{
        if (call_count == 0) {{
            call_count += 1
            this.context.eax = {hex(int_percent * 10)}
            console.log('Set energy {int_percent}');
        }}
    }}
    Interceptor.attach(dynamic_address_of_00415363, function_to_call_when_code_reaches_00415363); 
    Interceptor.flush();
"""

def set_time(hour):
    hex_hour = hex(hour - 1)
    return f"""
    var module_name_FiveNightsatFreddys_exe={MODULE_NAME};
    var n = 0;
    var offset_of_00415387=0x15391;
    var dynamic_address_of_00415387=Module.findBaseAddress(module_name_FiveNightsatFreddys_exe).add(offset_of_00415387);
    function function_to_call_when_code_reaches_00415387(){{
        if (n == 0) {{
            this.context.eax=0x59
            n = 1
        }} else if (n == 1) {{
            console.log('Set time {hour}')
            this.context.eax={hex_hour}
            n = 2
        }} else {{
            n = 3
        }}
    }}
    Interceptor.attach(dynamic_address_of_00415387, function_to_call_when_code_reaches_00415387); 
    Interceptor.flush();
"""

def minutes():
    return f"""
    var module_name_FiveNightsatFreddys_exe={MODULE_NAME};
    var offset_of_004153e0=0x153e0;
    var dynamic_address_of_004153e0=Module.findBaseAddress(module_name_FiveNightsatFreddys_exe).add(offset_of_004153e0);
    function function_to_call_when_code_reaches_004153e0(){{
        var offset = '0x' + (parseInt(this.context.ecx, 16) + 522).toString(16);
        var a = Memory.readByteArray(ptr(offset), 1);
        var bytes = new Uint8Array(a).join("");
        console.log('Time until new hour: ' + (90 - (255 - bytes)));
    }}
    Interceptor.attach(dynamic_address_of_004153e0, function_to_call_when_code_reaches_004153e0); 
    Interceptor.flush();
"""

def stop_time():
    return f"""
    var module_name_FiveNightsatFreddys_exe={MODULE_NAME};
    var offset_of_004153e0=0x153e0;
    var dynamic_address_of_004153e0=Module.findBaseAddress(module_name_FiveNightsatFreddys_exe).add(offset_of_004153e0);
    function function_to_call_when_code_reaches_004153e0(){{
        var offset = '0x' + (parseInt(this.context.ecx, 16) + 522).toString(16);
        Memory.writeByteArray(ptr(offset), [0xff]);
        var a = Memory.readByteArray(ptr(offset), 1);
        var bytes = new Uint8Array(a).join("");
        console.log('Time until new hour: ' + (90 - (255 - bytes)));
    }}
    Interceptor.attach(dynamic_address_of_004153e0, function_to_call_when_code_reaches_004153e0); 
    Interceptor.flush();
"""

def door_hack():
    return f"""
    var module_name_FiveNightsatFreddys_exe={MODULE_NAME};

    var addr;
    var find = false;
    var offset_of_0041c1ce=0x1c1ce;
    var dynamic_address_of_0041c1ce=Module.findBaseAddress(module_name_FiveNightsatFreddys_exe).add(offset_of_0041c1ce);
    function function_to_call_when_code_reaches_0041c1ce(){{
        if (this.context.eax == 0x4) {{
            console.log("Find door");
            addr = this.context.esi;
            find = true
        }}
        if (find == true && (this.context.esi.toString() == addr.toString())) {{
            console.log("Door is locked");
            this.context.eax = 0x2
        }}
    }}
    Interceptor.attach(dynamic_address_of_0041c1ce, function_to_call_when_code_reaches_0041c1ce); 
    Interceptor.flush();
"""

if __name__ == '__main__':
    main(PROC_NAME)
