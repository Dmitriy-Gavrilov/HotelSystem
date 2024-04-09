#include "findroombyequipmentform.h"
#include "ui_findroombyequipmentform.h"

FindRoomByEquipmentForm::FindRoomByEquipmentForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::FindRoomByEquipmentForm)
{
    ui->setupUi(this);
}

FindRoomByEquipmentForm::~FindRoomByEquipmentForm()
{
    delete ui;
}

void FindRoomByEquipmentForm::clear()
{
    this->ui->equipment->clear();
}

void FindRoomByEquipmentForm::on_FindRoomByEquipmentBtn_clicked()
{
    QString data = "findRoomByEquipment;" + this->ui->equipment->text();
    qDebug() << data << Qt::endl;
    emit sendData(data);
}

