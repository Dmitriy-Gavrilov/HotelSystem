#include "deleteroomform.h"
#include "ui_deleteroomform.h"

DeleteRoomForm::DeleteRoomForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DeleteRoomForm)
{
    ui->setupUi(this);
}

DeleteRoomForm::~DeleteRoomForm()
{
    delete ui;
}

void DeleteRoomForm::clear()
{
    this->ui->roomId->clear();
}

void DeleteRoomForm::on_deleteRoomBtn_clicked()
{
    QString data = "deleteRoom;" + this->ui->roomId->text();
    emit sendData(data);
}

