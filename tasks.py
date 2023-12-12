from robocorp.tasks import task
from robocorp import browser, http
from RPA.PDF import PDF
from RPA.FileSystem import FileSystem
from RPA.Archive import Archive
from libaries import DB
from progress.bar import Bar
from RPA.Tables import Tables

tables = Tables()

@task
def Order_robots_RobotSpareBin_Industries_Inc():
    """Solve the RPA challenge"""
    delete_files()
    get_order()
    #Inser into to database
    #DB.DB()
    pagina = login()
    read_csv_file(pagina)
    create_zip()


def login():
    browser.configure(
        screenshot="only-on-failure",
        headless=True,
        slowmo=100,
    )

    browser.goto("https://robotsparebinindustries.com/")
    pagina = browser.page()  
    pagina.wait_for_selector('//button[@class="btn btn-primary"]')
    pagina.click(selector='//a[@class="nav-link"]')
    pagina.wait_for_selector('//div[@class="alert-buttons"]')
    return pagina


def get_order():
    http.download("https://robotsparebinindustries.com/orders.csv", target_file="output/orders.csv", overwrite=True)


def read_csv_file(page):
    print("\n")
    #table_csv = DB.obtain_dat()
    table_csv = tables.read_table_from_csv(path='output/orders.csv')
    bar1 = Bar('Procesando:', max=20)
    for item in table_csv:
        page = place_values(pagina=page, dat=item)
        parar = True
        count = 0
        while parar:
            result = clic_order(page)
            if count == 15:
                parar = False
                break  
            if result:
                parar = False
                break
            else:
                count += 1
                continue
        Img_Pdf(page, item)
        bar1.next()
    bar1.finish()


def place_values(pagina, dat): 
    #------------------------------------------------------------------
    head = dat['Head']
    body = dat['Body']
    legs = dat['Legs']
    address = dat['Address']
    #------------------------------------------------------------------
    pagina.wait_for_selector('//button[@class="btn btn-dark"]')
    pagina.click(selector='//button[@class="btn btn-dark"]')
    pagina.wait_for_selector(selector='//select[@id="head"]')
    pagina.select_option(selector='//select[@id="head"]', value=f'{head}') 
    pagina.click(selector=f'//input[@id="id-body-{body}"]')
    pagina.fill(selector='//input[@placeholder="Enter the part number for the legs"]', value=f'{legs}')
    pagina.fill(selector='//input[@id="address"]', value=f'{address}')
    pagina.click(selector='//button[@id="preview"]')
    pagina.wait_for_selector(selector='//div[@id="robot-preview-image"]')
    return pagina
    #------------------------------------------------------------------


def clic_order(pagina):
    try:
        pagina.click(selector='//button[@id="order"]')
        pagina.wait_for_selector(selector='//div[@id="receipt"]')
        return True
    except:
        return False


def Img_Pdf(page, dat):
    pdf = PDF()
    order_nurmer = dat['Order number']
    page.locator('//div[@id="robot-preview-image"]').screenshot(path=f'IMG/image_robot_{order_nurmer}.png')
    sales_results_html = page.locator(selector='xpath=//div[@id="receipt"]').inner_html()
    pdf.html_to_pdf(sales_results_html, f'PDF/pdf_robot_{order_nurmer}.pdf')
    files = [f'IMG/image_robot_{order_nurmer}.png']
    pdf.open_pdf(f'PDF/pdf_robot_{order_nurmer}.pdf')
    pdf.add_files_to_pdf(files=files, target_document=f'PDF/pdf_robot_{order_nurmer}.pdf', append=True)
    pdf.close_all_pdfs()
    page.click('//button[@id="order-another"]')
    

def delete_files():
    fileSystem = FileSystem()
    #Eliminar IMAGENES
    listfileIMG = fileSystem.list_files_in_directory(path="IMG")
    for file in listfileIMG:
        fileSystem.remove_file(path=f'{file}')
    #Eliminar PDF'S
    listfilePDF = fileSystem.list_files_in_directory(path="PDF")
    for file in listfilePDF:
        fileSystem.remove_file(path=f'{file}')


def create_zip():
    archive = Archive()
    fileSystem = FileSystem()
    exist = fileSystem.does_directory_exist('resultado')
    if exist:
        fileSystem.remove_directory('resultado')
    fileSystem.create_directory('resultado')
    archive.archive_folder_with_zip(folder='PDF', archive_name='resultado/PDFS_robots.zip')


# if __name__ == '__main__':
#     Order_robots_RobotSpareBin_Industries_Inc()
