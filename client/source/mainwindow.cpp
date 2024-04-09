#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->ui->tabWidget->setCurrentIndex(0); // При запуске будет видна первая вкладка

    // Формы действий с гостями
    addGuestform = new addGuestForm();
    deleteGuestForm = new DeleteGuestForm();
    findGuestByIdForm = new FindGuestByIdForm();
    findGuestByFioForm = new FindGuestByFioForm();

    // Формы действий с комнатами
    addRoomForm = new AddRoomForm();
    deleteRoomForm = new DeleteRoomForm();
    findRoomByIdForm = new FindRoomByIdForm();
    findRoomByEquipmentForm = new FindRoomByEquipmentForm();

    // Формы регистраций
    moveInForm = new MoveInForm();
    departForm = new DepartForm();

    // Создание словаря с формами
    formsMap["addGuestform"] = addGuestform;
    formsMap["deleteGuestForm"] = deleteGuestForm;
    formsMap["findGuestByIdForm"] = findGuestByIdForm;
    formsMap["findGuestByFioForm"] = findGuestByFioForm;
    formsMap["addRoomForm"] = addRoomForm;
    formsMap["deleteRoomForm"] = deleteRoomForm;
    formsMap["findRoomByIdForm"] = findRoomByIdForm;
    formsMap["findRoomByEquipmentForm"] = findRoomByEquipmentForm;
    formsMap["moveInForm"] = moveInForm;
    formsMap["departForm"] = departForm;

    // Запуск серверной части программы
    pythonProcess = new QProcess(this);
    pythonProcess->start("C:/Users/Dmitriy/PycharmProjects/AirTickets/venv/Scripts/python.exe", QStringList() << "C:/Users/Dmitriy/PycharmProjects/AirTickets/main.py");




    socket = new class QTcpSocket(this); // Создание сокета

    connect(socket, &QTcpSocket::readyRead, this, &MainWindow::readResponse); //Вызов метода, когда в сокете
                                                                            //появляются данные для чтения

    // Соединение кнопок на формах с методом отправления данных
    connect(addGuestform, &addGuestForm::sendData, this, &MainWindow::sendRequest);
    connect(deleteGuestForm, &DeleteGuestForm::sendData, this, &MainWindow::sendRequest);
    connect(findGuestByIdForm, &FindGuestByIdForm::sendData, this, &MainWindow::sendRequest);
    connect(findGuestByFioForm, &FindGuestByFioForm::sendData, this, &MainWindow::sendRequest);

    connect(addRoomForm, &AddRoomForm::sendData, this, &MainWindow::sendRequest);
    connect(deleteRoomForm, &DeleteRoomForm::sendData, this, &MainWindow::sendRequest);
    connect(findRoomByIdForm, &FindRoomByIdForm::sendData, this, &MainWindow::sendRequest);
    connect(findRoomByEquipmentForm, &FindRoomByEquipmentForm::sendData, this, &MainWindow::sendRequest);

    connect(moveInForm, &MoveInForm::sendData, this, &MainWindow::sendRequest);
    connect(departForm, &DepartForm::sendData, this, &MainWindow::sendRequest);

    getRegistrations();
}

MainWindow::~MainWindow()
{
    delete ui;

    // Освобождение памяти, выделенной для форм
    delete addGuestform;
    delete deleteGuestForm;
    delete findGuestByIdForm;
    delete findGuestByFioForm;

    delete addRoomForm;
    delete deleteRoomForm;
    delete findRoomByIdForm;
    delete findRoomByEquipmentForm;

    delete moveInForm;
    delete departForm;

    // Закрытие сокета
    socket->close();
    delete socket;

    // Удаление процесса
    pythonProcess->deleteLater();
}

void MainWindow::closeEvent(QCloseEvent *event)
{
    sendRequest("quit"); // Запрос на закрытие сервера
    QMainWindow::closeEvent(event); // Закрытие окна
}

void MainWindow::getRegistrations()
{
    sendRequest("getRegistrations");
}

// Отправление данных на сервер
void MainWindow::sendRequest(const QString &request)
{
    QByteArray requestData = request.toUtf8();
    socket->connectToHost("localhost", 5050); // Подключение к серверу
    socket->waitForConnected(2500);
    socket->write(requestData);

    clearDisplay();
}

// Получение ответа от сервера
bool MainWindow::readResponse()
{
    QByteArray responseData = socket->readAll();
    QString responseStr = QString::fromUtf8(responseData);
    QStringList responseList = responseStr.split(";");
    bool isSuccess = (responseList[0] == "True");
    QString msg = responseList[1];
    QString formName = responseList[2];

    if (responseList.size() == 6) {
        displayData(responseList[3], responseList[4]);
        return isSuccess;
    }

    if (isSuccess) {
        closeForm(formName);
        QMessageBox::information(nullptr, "Информация об операции", msg);
        if (responseList.size() == 5){
            displayData(responseList[3], responseList[4]);
        }
    }
    else {
        QMessageBox::critical(nullptr, "Информация об операции", msg);
    }


    clearForm(formName);

    return isSuccess;
}

// Отображение результатов
void MainWindow::displayData(QString tabChoice, QString data)
{
    if (tabChoice == "findGuest"){
        this->ui->resultTextBrowser->setText(data);
    }
    else if (tabChoice == "findRoom"){
        this->ui->textBrowser->setText(data);
    }
    else{
        this->ui->textBrowser_3->setText(data);
    }
}

// Закрытие форм
void MainWindow::closeForm(QString name)
{
    if (formsMap.contains(name)){
        formsMap.value(name)->close();
    }
}

// Очистка данных на формах
void MainWindow::clearForm(QString name)
{
    if (formsMap.contains(name)){
        QWidget *widget = formsMap.value(name);
        BaseForm *baseForm = dynamic_cast<BaseForm*>(widget);
        baseForm->clear();
    }
}

// Очистка виджетов на главном окне
void MainWindow::clearDisplay()
{
    this->ui->resultTextBrowser->clear();
    this->ui->textBrowser->clear();
}

// Обработка нажатия на кнопки

void MainWindow::on_addGuest_clicked()
{
    this->addGuestform->setWindowModality(Qt::ApplicationModal); // Блокирует действия для других окон
    this->addGuestform->show();
}

void MainWindow::on_deleteGuest_clicked()
{
    this->deleteGuestForm->setWindowModality(Qt::ApplicationModal);
    this->deleteGuestForm->show();
}


void MainWindow::on_findGuestById_clicked()
{
    this->findGuestByIdForm->setWindowModality(Qt::ApplicationModal);
    this->findGuestByIdForm->show();
}


void MainWindow::on_findGuestByFio_clicked()
{
    this->findGuestByFioForm->setWindowModality(Qt::ApplicationModal);
    this->findGuestByFioForm->show();
}

void MainWindow::on_findRoomById_clicked()
{
    this->findRoomByIdForm->setWindowModality(Qt::ApplicationModal);
    this->findRoomByIdForm->show();
}


void MainWindow::on_findRoomByEquipment_clicked()
{
    this->findRoomByEquipmentForm->setWindowModality(Qt::ApplicationModal);
    this->findRoomByEquipmentForm->show();
}


void MainWindow::on_findAllGuests_clicked()
{
    sendRequest("findAllGuests");
}


void MainWindow::on_clearGuests_clicked()
{
    sendRequest("clearGuests");
}

void MainWindow::on_addRoom_clicked()
{
    this->addRoomForm->setWindowModality(Qt::ApplicationModal);
    this->addRoomForm->show();
}

void MainWindow::on_deleteRoom_clicked()
{
    this->deleteRoomForm->setWindowModality(Qt::ApplicationModal);
    this->deleteRoomForm->show();
}

void MainWindow::on_findAllRooms_clicked()
{
    sendRequest("findAllRooms");
}


void MainWindow::on_clearRooms_clicked()
{
    sendRequest("clearRooms");
}


void MainWindow::on_moveIn_clicked()
{
    this->moveInForm->setWindowModality(Qt::ApplicationModal);
    this->moveInForm->show();
}


void MainWindow::on_depart_clicked()
{
    this->departForm->setWindowModality(Qt::ApplicationModal);
    this->departForm->show();
}

