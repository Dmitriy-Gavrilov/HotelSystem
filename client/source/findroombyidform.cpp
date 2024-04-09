#include "findroombyidform.h"
#include "ui_findroombyidform.h"

FindRoomByIdForm::FindRoomByIdForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::FindRoomByIdForm)
{
    ui->setupUi(this);
}

FindRoomByIdForm::~FindRoomByIdForm()
{
    delete ui;
}

void FindRoomByIdForm::clear()
{
    this->ui->roomId->clear();
}

void FindRoomByIdForm::on_FindRoomByIdBtn_clicked()
{
    QString data = "findRoomById;" + this->ui->roomId->text();
    emit sendData(data);
}

