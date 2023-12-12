from robocorp.tasks import task
from RPA.Windows import Windows
from RPA.Desktop import Desktop

windows = Windows()
desktop = Desktop()

@task
def interaction_windows():
    #Locator padre
    locator = "type:window class:CabinetWClass > class:ShellTabWindowClass > class:DUIViewWndClassName"
    #Abrir explorer
    explorer = desktop.open_application(name_or_path='explorer.exe')
    #Espera a una ventana y fijarla como principal
    windows.control_window(locator='type:window class:CabinetWClass', timeout=30.0)
    #Clic a un elemento
    windows.click(locator=f'{locator} > class:ProperTreeHost > class:SysTreeView32 > path:2|9')
    #Espera de elementos
    windows.set_anchor(locator=f'{locator} > class:DUIListView', timeout=30.0)
    #Clic derecho
    windows.click(locator=f'{locator} > class:DUIListView > path:1 > class:UIItem name:"Paso a paso ejecución robot"')
    #Copiar documento
    windows.send_keys(locator=f'{locator} > class:DUIListView > path:1 > class:UIItem name:"Paso a paso ejecución robot"', keys="{CTRL}{C}")
    #CLic en Update
    windows.click(locator=f'{locator} > class:ProperTreeHost > class:SysTreeView32 > path:2|12')
    #Pegar documento
    windows.send_keys(locator=f'{locator} > class:DUIListView > path:1', keys="{CTRL}{V}")
    #Cerrar ventana
    windows.close_window(locator='type:window class:CabinetWClass')
    #Imprimir arbol de elemento
    tree = windows.print_tree(f'{locator} > class:ProperTreeHost > class:SysTreeView32', return_structure=True)
    print(tree)


