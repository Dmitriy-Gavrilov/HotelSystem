#ifndef ADDROOMFORM_H
#define ADDROOMFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class AddRoomForm;
}

class AddRoomForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit AddRoomForm(QWidget *parent = nullptr);
    ~AddRoomForm();

    void clear() override;

signals:
    void sendData(const QString &data);

private slots:
    void on_addRoomBtn_clicked();

private:
    Ui::AddRoomForm *ui;
};

#endif // ADDROOMFORM_H
