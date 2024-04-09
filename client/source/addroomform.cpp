#include "addroomform.h"
#include "ui_addroomform.h"

AddRoomForm::AddRoomForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::AddRoomForm)
{
    ui->setupUi(this);
}

AddRoomForm::~AddRoomForm()
{
    delete ui;
}

void AddRoomForm::clear()
{
    this->ui->roomId->clear();
    this->ui->capacity->setValue(1);
    this->ui->roomsCount->setValue(1);
    this->ui->bathroom->setCurrentIndex(0);
    this->ui->equipment->clear();
}

void AddRoomForm::on_addRoomBtn_clicked()
{
    QString data = "addRoom;" + this->ui->roomId->text() + ";" + this->ui->capacity->text() + ";" +
                   this->ui->roomsCount->text() + ";" + QString::number(this->ui->bathroom->currentIndex()) +
                   ";" + this->ui->equipment->text();

    emit sendData(data);
}

